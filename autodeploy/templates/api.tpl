
<h1>API endpoints</h1>

<p>These return JSON</p>

<table class="table table-bordered">
 <tbody>

  <tr>
   <td>/check/&lt;server&gt;/&lt;branch&gt;</td>
   <td>Check if a given branch can be deployed to the given server</td>
  <tr>

  <tr>
   <td>/deploy/&lt;server&gt;/&lt;branch&gt;</td>
   <td>Deploy the given branch to the given server</td>
  <tr>

  <tr>
   <td>/merge/&lt;server&gt;/&lt;branch&gt;</td>
   <td>Merge a deployed branch into master and switch server to master</td>
  <tr>

  <tr>
   <td>/servers</td>
   <td>List configured servers</td>
  <tr>

  <tr>
   <td>/branches</td>
   <td>List unmerged branches</td>
  <tr>

 </tbody>
</table>

<h1>Pages</h1>

<p>These return HTML. You can pass ?headless=1 to all except / to skip html/body and return only contents for use as an ajax flake.</p>

<table class="table table-bordered">
 <tbody>

  <tr>
   <td>/</td>
   <td>Front page</td>
  <tr>

  <tr>
   <td>/show/&lt;id&gt;</td>
   <td>Show details for an action</td>
  <tr>

  <tr>
   <td>/help/&lt;topic&gt;</td>
   <td>Help pages - maps to files in templates/help-&lt;topic&gt;.tpl</td>
  <tr>

  <tr>
   <td>/static/&lt;path&gt;</td>
   <td>Static resources - maps to files in static/</td>
  <tr>

 </tbody>
</table>

<h1>Authentication</h1>

<ul>
 <li>Basic auth is used to authenticate users</li>
 <li>Users should be added to user-section in /etc/autodeploy/config.json</li>
 <li>Authentication could be made pluggable, but should not be removed, since we need a username to log actions by</li>
</ul>
