import os
import sys

def update_frontmatter(post_path, at_uri):
    """Add blueskyPostURI to the frontmatter of a blog post."""
    try:
        with open(post_path, 'r') as f:
            content = f.read()
        
        if content.startswith('---\n'):
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if i > 0 and line.strip() == '---':
                    lines.insert(i, f'blueskyPostURI: "{at_uri}"')
                    break
            
            with open(post_path, 'w') as f:
                f.write('\n'.join(lines))
            print(f"Updated {post_path} with blueskyPostURI")
            return True
        else:
            print("Error: Post doesn't start with frontmatter")
            return False
            
    except Exception as e:
        print(f"Error updating frontmatter: {e}")
        return False

if __name__ == "__main__":
    post_path = os.environ.get('POST_PATH')
    at_uri = os.environ.get('AT_URI')
    
    if not post_path or not at_uri:
        print("Error: POST_PATH and AT_URI environment variables required")
        sys.exit(1)
    
    success = update_frontmatter(post_path, at_uri)
    sys.exit(0 if success else 1)