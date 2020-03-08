# Gitflow

This project uses a simplified version of the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).

### Creating an issue
1. Navigate to the "Issues" tab on GitHub and click "New issue"
2. Choose the appropriate template
3. Add appropriate description
4. Add appropriate label
   - "feature" and "bug" for respective types of issues
   - "feedback" for feedback related change
   - "documentation" for documenation related change
5. Assign the appropriate person/s

### Typical procedure for working on a new feature
1. Pick an issue to work on from backlog in [ZenHub](https://app.zenhub.com/login).
    - Remember to move the issue to "In Progress" on [ZenHub](https://app.zenhub.com/login).
2. Create a new branch from `develop`, with the following naming convention: `ISSUE_TYPE/ISSUE_ID-name-of-branch`.
    - Example feature branch name: `feature/278-user-login-screen`
    - Example bugfix branch name: `bugfix/26-menu-glitches`
3. Work on feature and commit/push to this branch. 
    - Keep in mind that other developers may merge changes into `develop` while you are developing, remember to `git merge develop` if necessary and appropriate.
4. Once work is complete, open a pull request (PR) from your branch to `develop` from GitHub. At least 1 other developer has to approve the PR, and all reviewers assigned to the PR must approve before the PR can be merged.
    - Remember to link your PR to the corresponding issue on [ZenHub](https://app.zenhub.com/login).
5. Once your branch is merged with `develop`, delete the branch.

### Release procedure
1. The features to be included in the next release will be discussed in a team meeting.
2. A release branch will be made wih the following naming convention: `release/RELEASE_NUMBER-release-feature-summary`.
3. After any changes to the code on the branch has been made and verified, a PR will be made from the release branch to both `develop` and `master`. At least 2 developers have to approve the PR, and all reviewers assigned to the PR must approve before the PR can be merged.
4. The release branch will be deleted after it has been merged.

# ZenHub

This project uses [ZenHub](https://www.zenhub.com/) as its issue board. ZenHub is linked to GitHub and changes to issues/PRs on GitHub will be reflected on the ZenHub board.

### ZenHub notes for developers
- After you've merged a `feature`/`bugfix` branch into `develop`, move the card on ZenHub to "Done", not "Closed". We will close issues from "Done" during our sprint close meetings.