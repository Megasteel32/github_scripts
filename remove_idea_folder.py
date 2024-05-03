from github import Github

# Replace with the path to the file containing your GitHub access token
access_token_file = 'access_token.txt'

# Replace with your GitHub username
username = 'megasteel32'

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

# Iterate over the user's repositories and print the tree structure
# for repo in repos:
#     print(f"\nRepository: {repo.name}")
#     print("Tree structure:")
#
#     def print_tree(contents, level=0):
#         for content in contents:
#             indent = '  ' * level
#             if content.type == 'dir':
#                 print(f"{indent}📁 {content.name}")
#                 sub_contents = repo.get_contents(content.path)
#                 print_tree(sub_contents, level + 1)
#             else:
#                 print(f"{indent}📄 {content.name}")
#
#     try:
#         contents = repo.get_contents('')
#         print_tree(contents)
#     except Exception as e:
#         print(f"Error occurred while retrieving contents of repository {repo.name}: {str(e)}")

# Ask for confirmation before proceeding
confirmation = input("\nDo you want to proceed with removing the folder containing 'idea' from these repositories? (y/n): ")

if confirmation.lower() == 'y':
    # Iterate over the user's repositories
    for repo in repos:
        try:
            # Get the contents of the entire repository
            contents = repo.get_contents('')

            # Search for a folder that contains "idea"
            idea_folder = None
            for content in contents:
                if content.type == 'dir' and 'idea' in content.name.lower():
                    idea_folder = content
                    break

            if idea_folder:
                # Recursively delete the contents of the "idea" folder
                def delete_folder_contents(folder_path):
                    folder_contents = repo.get_contents(folder_path)
                    for content in folder_contents:
                        if content.type == 'dir':
                            delete_folder_contents(content.path)
                        else:
                            repo.delete_file(content.path, "Remove 'idea' folder", content.sha)

                delete_folder_contents(idea_folder.path)

                # Delete the "idea" folder itself
                repo.delete_file(idea_folder.path, "Remove 'idea' folder", idea_folder.sha)

                print(f"Removed folder containing 'idea' from repository {repo.name}.")
            else:
                print(f"Repository {repo.name} does not have a folder containing 'idea'.")
        except Exception as e:
            print(f"Error occurred while processing repository {repo.name}: {str(e)}")
else:
    print("Operation canceled.")