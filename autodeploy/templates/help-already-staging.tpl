% if not data['headless']:
    % include templates/header
% end

<div class="help-container">

    <h2>Server should not already be staging</h2>

    <p>
    New branches are deployed in production for a little while before they are
    merged into master. This way we always have a clean master we can roll back to.
    </p>

    <p>
    This staging phase should however be relatively short lived, and we should take care
    to stage and merge one branch at a time. This is important because the merging of
    one branch may affect deployability of another branch. So if we switch from branch A
    to B, merge B, and switch back to A, then A may not really be deployable anymore.
    </p>

    <p>
    Therefore we disallow new deploys while server is staging a branch.
    </p>

    <img src="/static/server-locked-during-staging.png"/>

    <h3>How to fix it</h3>

    Check which branch is blocking us:
<pre>
[fuzz] !deploy servers
[Autobot] Servers and their branches:
[Autobot] * production - my-super-branch
[Autobot] * dev2 - master</pre>

    Merge it:

<pre>
[fuzz] !deploy merge my-super-branch production
[Autobot] Merged</pre>

    Make sure you <b>check with the team</b> that the branch can be merged first!

</div>

% if not data['headless']:
    % include templates/header
% end
