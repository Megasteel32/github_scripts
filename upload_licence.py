from github import Github

# Replace with the path to the file containing your GitHub access token
access_token_file = 'access_token.txt'

# Replace with your GitHub username
username = 'megasteel32'

# Read the content of the LICENSE.MARKDOWN file from the same directory
license_file = 'LICENSE.MARKDOWN'
with open(license_file, 'r', encoding='utf-8') as file:
    license_content = file.read()

# Read the access token from the file
if access_token_file:
    with open(access_token_file, 'r') as file:
        access_token = file.read().strip()
else:
    access_token = input("Enter your GitHub access token: ")

# Create a PyGithub instance
g = Github(access_token)

# Get the user object
user = g.get_user(username)

# Get the list of repositories
repos = list(user.get_repos())

# Print the list of repositories
print("Repositories:")
for repo in repos:
    print(f"- {repo.name}")

# Ask for confirmation before proceeding
confirmation = input("Do you want to proceed with adding the LICENSE.MARKDOWN file to these repositories? (y/n): ")

if confirmation.lower() == 'y':
    # Iterate over the user's repositories
    for repo in repos:
        # Check if the repository already has a LICENSE.MARKDOWN file
        try:
            repo.get_contents('LICENSE.MARKDOWN')
            print(f"Repository {repo.name} already has a LICENSE.MARKDOWN file.")
        except:
            # Create the LICENSE.MARKDOWN file in the repository
            repo.create_file('LICENSE.MARKDOWN', 'Add LICENSE.MARKDOWN', license_content)
            print(f"Added LICENSE.MARKDOWN to repository {repo.name}.")
else:
    print("Operation canceled.")