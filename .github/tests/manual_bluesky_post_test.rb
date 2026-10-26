require 'minitest/autorun'
require 'yaml'
require 'open3'
require 'tempfile'

class ManualBlueskyPostTest < Minitest::Test
  ROOT = File.expand_path('../..', __dir__)
  POST_FILE = '2026-10-24-mvp-gyropalooza-2026.md'
  POST_URL = 'https://rawlinson.us/fun/mvp-gyropalooza-2026/#page-title'
  DESCRIPTION = "Gyropalooza from a discgolfer perspective - a discgolfer who isn't an MVP fanatic"

  def prepare_message(response, check_prompt: false)
    workflow = YAML.load_file(File.join(ROOT, '.github/workflows/manual-bluesky-post.yml'))
    step = workflow.fetch('jobs').fetch('post-to-bluesky').fetch('steps').find do |candidate|
      candidate['id'] == 'prepare'
    end
    script = step.fetch('run')
      .gsub('${{ github.event.inputs.post_file }}', POST_FILE)
      .gsub('${{ github.event.inputs.custom_message }}', '')

    stubs = <<~'BASH'
      sudo() { return 0; }
      curl() {
        if [ "$CHECK_PROMPT" = "true" ]; then
          while [ "$#" -gt 0 ]; do
            if [ "$1" = "-d" ]; then
              printf '%s' "$2" | jq -e '.messages[0].content | contains("Title: MVP Gyropalooza 2026.") and contains("Description: Gyropalooza from a discgolfer perspective")' >/dev/null || return 1
              break
            fi
            shift
          done
        fi
        printf '%s' "$AI_RESPONSE_FIXTURE"
      }
    BASH

    Tempfile.create('bluesky-output') do |output|
      stdout, stderr, result = Open3.capture3(
        {
          'AI_RESPONSE_FIXTURE' => response,
          'CHECK_PROMPT' => check_prompt.to_s,
          'GITHUB_OUTPUT' => output.path,
          'GITHUB_TOKEN' => 'offline-test'
        },
        'bash', '-e', '-o', 'pipefail', '-c', stubs + script,
        chdir: ROOT
      )
      assert result.success?, "Prepare step failed (#{result.exitstatus}):\n#{stdout}\n#{stderr}"
      File.read(output.path).strip
    end
  end

  def test_plain_text_response_uses_description
    assert_equal "MESSAGE=#{DESCRIPTION} #{POST_URL}", prepare_message('OK')
  end

  def test_empty_response_uses_description
    assert_equal "MESSAGE=#{DESCRIPTION} #{POST_URL}", prepare_message('')
  end

  def test_non_object_json_uses_description
    assert_equal "MESSAGE=#{DESCRIPTION} #{POST_URL}", prepare_message('[]')
  end

  def test_api_error_uses_description
    response = '{"error":{"message":"Rate limit exceeded"}}'
    assert_equal "MESSAGE=#{DESCRIPTION} #{POST_URL}", prepare_message(response)
  end

  def test_missing_ai_content_uses_description
    assert_equal "MESSAGE=#{DESCRIPTION} #{POST_URL}", prepare_message('{}')
  end

  def test_successful_response_uses_ai_content_and_frontmatter_prompt
    response = '{"choices":[{"message":{"content":"A visit to Gyropalooza."}}]}'
    assert_equal "MESSAGE=A visit to Gyropalooza. #{POST_URL}", prepare_message(response, check_prompt: true)
  end
end