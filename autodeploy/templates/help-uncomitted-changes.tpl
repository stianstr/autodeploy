% if not data['headless']:
    % include templates/header
% end

<div class="help-container">

    <h2>Server should not have uncomitted changes</h2>

    <p>
    If we edit files on the production server, they <b>must be committed immediately</b>.
    </p>

    <p>
    If we don't then these changes will be kept around when we stage a branch, meaning
    that what we observe during staging is not really the branch code, but the branch
    code overlayed by these uncomitted changes.
    </p>

    <p>
    We may be in for a surprise after branch has been merged, which is a Bad Thing:
    </p>

    <img src="/static/uncomitted.png"/>

    <h3>How to fix</h3>
    Commit and push the changes
    <pre>
# on the production server
git commit -a -m 'Committing changes that some idiot left on production server'
git push</pre>

</div>

% if not data['headless']:
    % include templates/header
% end
