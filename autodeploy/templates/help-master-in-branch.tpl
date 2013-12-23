% if not data['headless']:
    % include templates/header
% end

<div class="help-container">

    <h2>Branch should contain master</h2>

    <p>Your branch should have <b>merged in the latest changes from master</b> before you deploy it.</p>

    <h3 class="wrong">If you don't then this may happen:</h3>
    <img src="/static/master-not-in-branch.png"/>

    <h3 class="correct">If you do then this will happen:</h3>
    <img src="/static/master-in-branch.png"/>

    <h3>How to fix it</h3>

    If you're working solo:
    <pre>
    # inside your branch
    git rebase master
    </pre>
    <div style="font-size: 10px">
    Using <a target="_new" href="http://git-scm.com/book/en/Git-Branching-Rebasing">rebase</a>,
    will basically jump to latest point in master and replay all your changes
    on top of there. That's great if you're working solo. But if other people has got your
    commits you can make life miserable for them by rebasing.
    </div>

    If other people has got your commits:
    <pre>
    # inside your branch
    git pull master
    </pre>
    <div style="font-size: 10px">
    This won't mess up things for those who has checked out your commits and based their work on them.
    </div>

    <div style="color: red">todo: should research this a bit more</div>

</div>

% if not data['headless']:
    % include templates/header
% end
