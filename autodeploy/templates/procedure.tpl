<h1>Deploy procedure</h1>

<span class="label label-danger">todo:</span> clean this up

<h3>Check that branch can be deployed</h3>
<ul>
 <li>Branch contains latest commit in master</li>
 <li>Repository at deploy-to-server does not have uncomitted changes</li>
 <li>Build status at CI server is green</li>
 <li>Branch deployed at deploy-to-server is master</li>
</ul>

<h3>Check branch deploy mode</h3>
<ul>
 <li>
  malicious
  <ul>
    <li>At least one DB update exist with mode:malicious, or</li>
    <li>At least one ENV update exist with mode:malicious, or</li>
    <li>Branch itself is tagged in git with mode:malicious</li>
  </ul>
 </li>
 <li>
  kind
  <ul>
   <li>At least one DB update exist with mode:kind, or</li>
   <li>At least one ENV update exist with mode:kind, or</li>
   <li>Branch itself is tagged in git with mode:kind</li>
  </ul>
 </li>
 <li>
  stealth
  <ul>
   <li>All updates have mode:stealth</li>
   <li>Branch itself is not tagged</li>
  </ul>
 </li>
</ul>
 
<h3>Deploy</h3>
<ul>
 <li>(Stop Apache if malicious, or hang Apache if kind)</li>
 <li>git pull</li>
 <li>Run ENV updates</li>
 <li>Run DB updates</li>
 <li>(Resume Apache if malicious or kind)</li>
</ul>

<h1>Update modes</h1>
<pre>
1. stealth

Can be run during daytime / while users are active,
without stopping the system. Effectively means that if:
a) user starts a request
b) update is run
c) user's request ends
..then this will never cause any problems.

This means that f.ex. renaming a field, does NOT fall into this category.
On the other hand, adding a new field that is not yet used by the code does.

2. kind

Can be run during daytime / while users are active,
but the system will ensure that no requests are processed
when the code and db state are not in a consistent state.

Basically means we:
- set all new requests to hang
- wait for all non-hanging requests to finish
- run code update
- run db/env updates
- release hanging requests (redirect to itself, causing them to be run in new code)

Criteria for such updates are that they are fairly quick, so hang-time will
be short (typically <5sec).

3. malicious

Slow or critical updates that should only be run during nighttime
/ when no users are on the system. Apache will be shut down entirely
during the update process.

</pre>
