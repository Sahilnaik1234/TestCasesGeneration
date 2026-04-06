from github import Github
import subprocess
import os

class GithubManager:
    def __init__(self, token: str, repo_name: str):
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)
    
    def close_pr(self, pr_number: int):
        pr = self.repo.get_pull(pr_number)
        pr.edit(state='closed')
        print(f"Closed PR #{pr_number}")
        return pr

    def create_pr(self, title: str, body: str, head_branch: str, base_branch: str):
        # check if PR already exists
        pulls = self.repo.get_pulls(state='open', head=f"{self.repo.owner.login}:{head_branch}", base=base_branch)
        if pulls.totalCount > 0:
            print(f"PR already exists: #{pulls[0].number}")
            return pulls[0].number
        
        new_pr = self.repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)
        print(f"Created new PR #{new_pr.number}")
        return new_pr.number

class GitHelper:
    @staticmethod
    def run_cmd(cmd: list):
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()

    @staticmethod
    def create_and_checkout_branch(new_branch_name: str):
        GitHelper.run_cmd(["git", "checkout", "-b", new_branch_name])
    
    @staticmethod
    def commit_and_push(branch_name: str, commit_message: str):
        GitHelper.run_cmd(["git", "add", "."])
        # Only commit if there are changes
        status = GitHelper.run_cmd(["git", "status", "--porcelain"])
        if not status:
            print("No changes to commit.")
            return False
        
        # Configure user if not exists (helpful in CI)
        subprocess.run(["git", "config", "user.name", "github-actions"], check=False)
        subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=False)
        
        GitHelper.run_cmd(["git", "commit", "-m", commit_message])
        GitHelper.run_cmd(["git", "push", "origin", "HEAD"])
        return True
