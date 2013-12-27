<h1>Background</h1>

<p>Autodeploy is based on <a href="https://github.com/blog/1241-deploying-at-github">githubs deployment procedure</a>. The key idea is that the <b>master branch is always stable</b>, and never worked on directly. Whenever you want to change something, you <b>always create a branch</b>. When the branch is ready, it should pass build+tests at the CI server (Jenkins or similar). When it has been successully built, the production server is switched from master to the branch. Stability is then observed for a while. If things look okay, then the branch is merged into master, and the server is switched back to master. If things go bad, we roll back to the always stable master.</p>

<p>This can of course be taken further, by f.ex. adding another staging step at a separate staging server. But either way, the branch should always be observed in production for a while before being merged into master, because from time to time, unexpected crap happens (only) in production.</p>

<h1>Workflow</h1>

<h2>1. Develop</h2>

<h4>1a. Create a new branch and work on it:</h4>

<pre>
# Create a branch and switch to it
git checkout -b my-cool-feature

# Work
echo 'syntax error' >>index.php

# Commit and push to branch
git commit -a -m 'Added nice features'
git push origin my-cool-feature

# After the first push, the branch is visible to others, and in autodeploy's web ui.
# Listing remote branches should show it:
git branch -r
</pre>

<p>Continue to work, commit, push. After you're done, changes may have happened to master, and you want to...</p>

<h4>1b. Merge in master</h4>
<p>There are two ways to do this; rebase or pull.</p>

<p>If you rebase, you basically stash all changes, update master, then apply all your changes on top of the recent master. If you work solo on your branch then that's probably best:</p>

<pre>
git rebase master
git commit -a -m 'Merged in master'
git push origin my-cool-feature
</pre>

<p>On the other hand, if you've already pushed commits and someone else is working on them, rebasing can make their life miserable. Then you'll rather want to merge the old-fashioned way:</p>

<pre>
git pull master
git commit -a -m 'Merged in master'
git push origin my-cool-feature
</pre>

Now you're almost ready to deploy. The CI server should pick up your latest push and build it. When it's done you can ask autodeploy to deploy your branch for staging.

<h2>2. Deploy for staging</h2>

<p>Ask Autodeploy to push your branch to the production server.</p>

Using IRC:
<pre>
!deploy push my-cool-feature production-server
</pre>

Using API:
<pre>
curl http://autodeploy.myhost.com/deploy/my-cool-feature/production-server
</pre>

<h4>Autodeploy will then run the following checks:</h4>

<h5>Branch should be of correct type</h5>
<ul>
 <li>Branch should exist</li>
 <li>Branch should not be master</li>
</ul>

<h5>Build status should be green</h5>
<ul>
 <li>CI server should have built latest revision of branch</li>
 <li>Status of that build should be OK (ie. all tests passed etc.)</li>
</ul>

<h5>Server should not have uncomitted changes</h5>
<ul>
 <li>When a branch is deployed for staging, the server we deploy to must not have uncomitted changes</li>
 <li><a onclick="autoDeploy.openHelpDialog('uncomitted-changes')">Explain why this is important</a></li>
</ul>

<h5>Branch should contain master</h5>
<ul>
 <li>Branch should contain everything that master does, in other words:</li>
 <li>The latest commit in master should also be in branch</li>
 <li><a onclick="autoDeploy.openHelpDialog('master-in-branch')">Explain why this is important</a></li>
</ul>

<h5>Server should not already be staging</h5>
<ul>
 <li>We should take care to only stage one branch at a time, so:</li>
 <li>The server we deploy to must not be staging another branch, it should be on master</li>
 <li><a onclick="autoDeploy.openHelpDialog('already-staging')">Explain why this is important</a></li>
</ul>

<p>If all these are ok, server will be switched to your branch. You should now observe logs and user feedback for a while. If things look ok, proceed to merge branch into master.</p>

<h2>3. Merge branch into master</h3>

<p>Ask Autodeploy to merge branch into master, and switch production server back to master.</p>

Using IRC:
<pre>
!deploy merge my-cool-feature production-server
</pre>

Using API:
<pre>
curl http://autodeploy.myhost.com/merge/my-cool-feature/production-server
</pre>

<h2>4. Goto 1</h2>

We're done. Production server is now ready to stage another branch.
