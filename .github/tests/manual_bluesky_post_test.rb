require 'minitest/autorun'
require 'yaml'
require 'open3'
require 'tempfile'
require 'date'

class ManualBlueskyPostTest < Minitest::Test
  ROOT = File.expand_path('../..', __dir__)
  POST_FILE = '2026-10-24-mvp-gyropalooza-2026.md'
  POST_URL = 'https://rawlinson.us/fun/mvp-gyropalooza-2026/#page-title'
  DESCRIPTION = YAML.safe_load(
    File.read(File.join(ROOT, '_posts', POST_FILE)).split(/^---$/, 3)[1],
    permitted_classes: [Date]
  ).fetch('description')

  def prepare_message(custom_message: '', workflow_file: 'manual-bluesky-post.yml', job: 'post-to-bluesky', step_id: 'prepare')
    workflow = YAML.load_file(File.join(ROOT, '.github/workflows', workflow_file))
    step = workflow.fetch('jobs').fetch(job).fetch('steps').find do |candidate|
      candidate['id'] == step_id
    end
    script = step.fetch('run')
    environment = step.fetch('env').transform_values do |value|
      value.gsub('${{ github.event.inputs.post_file }}', POST_FILE)
        .gsub('${{ github.event.inputs.custom_message }}', custom_message)
        .gsub('${{ needs.build-and-deploy.outputs.new-posts }}', "_posts/#{POST_FILE}")
    end

    stubs = <<~'BASH'
      sudo() { return 0; }
      curl() {
        echo 'Unexpected AI request' >&2
        printf '%s' '{"choices":[{"message":{"content":"AI must not be used."}}]}'
      }
    BASH

    Tempfile.create('bluesky-output') do |output|
      stdout, stderr, result = Open3.capture3(
        environment.merge('GITHUB_OUTPUT' => output.path),
        'bash', '-e', '-o', 'pipefail', '-c', stubs + script,
        chdir: ROOT
      )
      assert result.success?, "Prepare step failed (#{result.exitstatus}):\n#{stdout}\n#{stderr}"
      refute_includes stderr, 'Unexpected AI request'
      File.read(output.path).lines.map { |line| line.strip.split('=', 2) }.to_h
    end
  end

  def test_manual_workflow_uses_description_without_ai
    assert_equal "#{DESCRIPTION} #{POST_URL}", prepare_message.fetch('MESSAGE')
  end

  def test_automated_workflow_uses_description_without_ai
    outputs = prepare_message(workflow_file: 'jekyll.yml', job: 'bluesky-social', step_id: 'process-posts')
    assert_equal "#{DESCRIPTION} #{POST_URL}", outputs.fetch('BLUESKY_TEXT')
    assert_equal "_posts/#{POST_FILE}", outputs.fetch('POST_FILE')
  end

  def test_manual_custom_message_is_preserved
    message = 'A "custom" visit to Gyropalooza with $shell syntax.'
    assert_equal "#{message} #{POST_URL}", prepare_message(custom_message: message).fetch('MESSAGE')
  end

  def test_workflows_do_not_request_models_permission
    %w[manual-bluesky-post.yml jekyll.yml].each do |filename|
      workflow = YAML.load_file(File.join(ROOT, '.github/workflows', filename))
      refute workflow.fetch('permissions').key?('models'), "#{filename} still requests model access"
    end
  end
end