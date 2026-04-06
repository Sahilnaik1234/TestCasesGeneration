import argparse
import os
import sys

from src.coverage.parser import CoverageParser
from src.llm.provider import get_llm_provider
from src.generator.test_generator import TestGenerator
from src.github.manager import GithubManager, GitHelper

def main():
    parser = argparse.ArgumentParser(description="AI Test Generator")
    parser.add_argument("--coverage-file", required=True, help="Path to coverage.xml")
    parser.add_argument("--threshold", type=float, default=75.0, help="Coverage threshold")
    parser.add_argument("--pr-number", type=int, help="Current PR number to disable (close)")
    parser.add_argument("--repo", help="Repository name e.g. user/repo")
    parser.add_argument("--base-branch", default="dev", help="Base branch for the PR")
    parser.add_argument("--provider", default="groq", help="LLM Provider: groq, gemini, claude")
    
    args = parser.parse_args()

    # 1. Parse Coverage
    try:
        cov_parser = CoverageParser(args.coverage_file)
        overall_coverage = cov_parser.get_coverage_percentage()
        print(f"Overall Coverage: {overall_coverage}%")
        
        if overall_coverage >= args.threshold:
            print(f"Coverage is above threshold ({args.threshold}%). No action needed.")
            sys.exit(0)
            
        low_cov_files = cov_parser.get_files_with_low_coverage(args.threshold)
        print(f"Found {len(low_cov_files)} files below {args.threshold}% coverage.")
    except Exception as e:
        print(f"Error parsing coverage: {e}")
        sys.exit(1)

    if not low_cov_files:
        print("No specific files found below threshold. Exiting.")
        sys.exit(0)

    # 2. Get current branch (assuming we're running inside Github Actions PR event)
    current_head_branch = os.environ.get('GITHUB_HEAD_REF', 'local-feature-branch')
    target_branch = current_head_branch

    # Ensure we are on the feature branch for committing
    print(f"Checking out target branch: {target_branch}")
    try:
        GitHelper.run_cmd(["git", "checkout", target_branch])
    except Exception:
        # If the branch doesn't exist locally, fetch and checkout
        GitHelper.run_cmd(["git", "fetch", "origin", target_branch])
        GitHelper.run_cmd(["git", "checkout", target_branch])

    # 3. Generate Tests
    try:
        provider = get_llm_provider(args.provider)
        generator = TestGenerator(provider)
        generator.generate_tests_for_files(low_cov_files)
    except Exception as e:
        print(f"Error generating tests: {e}")
        sys.exit(1)

    # 4. Commit and Push
    commit_msg = "test: AI generated tests to boost coverage"
    pushed = GitHelper.commit_and_push(target_branch, commit_msg)

    if not pushed:
        print("No test files were generated or changed. Exiting.")
        sys.exit(0)

    # 5. Manage PRs
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_name = args.repo or os.environ.get('GITHUB_REPOSITORY')
    
    if github_token and repo_name:
        gh_manager = GithubManager(github_token, repo_name)
        
        # Close old PR
        if args.pr_number:
            gh_manager.close_pr(args.pr_number)
            
        # Open new PR
        title = f"AI Test Coverage Boost for {current_head_branch}"
        body = f"This PR contains AI-generated tests because coverage dropped below {args.threshold}%. It replaces the original PR."
        gh_manager.create_pr(title, body, target_branch, args.base_branch)
    else:
        print("GITHUB_TOKEN or GITHUB_REPOSITORY not set. Cannot manage PRs.")

if __name__ == "__main__":
    main()
