<!--
<h2>Last 10 successful deploys</h2>

<table class="table table-condensed">
 <thead>
  <tr>
   <th>Branch</th>
   <th>Server</th>
   <th>Time</th>
   <th>User</th>
   <th>ID</th>
  </tr>
 </thead>
 <tbody>
% for item in data['logDeploySuccess']:
  <tr>
   <td>{{item[3]}}</td>
   <td>{{item[2]}}</td>
   <td>{{item[0]}}</td>
   <td>{{item[1]}}</td>
   <td><a href="/show/{{item[4]}}">{{item[4]}}</a></td>
  </tr>
% end
 </tbody>
</table>
-->

<h2>Last 10 actions</h2>

<table class="table table-condensed">
 <thead>
  <tr>
   <th>Status</th>
   <th>Branch</th>
   <th>Server</th>
   <th>Action</th>
   <th>Time</th>
   <th>User</th>
   <th>ID</th>
  </tr>
 </thead>
 <tbody>
% for item in data['logAll']:
  <tr
  % if data['highlight'] and data['highlight'] == item[6]:
    class="warning"
  % end
  >
   <td>
    % if item[5] == 'success':
        <span class="label label-success">
    % else:
        <span class="label label-danger">
    % end
    {{item[5]}}
    </span>
   </td>
   <td>{{item[4]}}</td>
   <td>{{item[3]}}</td>
   <td>{{item[2]}}</td>
   <td>{{item[0]}}</td>
   <td>{{item[1]}}</td>
   <td><a onclick="autoDeploy.openShowDialog('{{item[6]}}')">{{item[6]}}</a></td>
  </tr>
% end
 </tbody>
</table>

<h2>Active branches</h2>

<table class="table table-condensed">
 <thead>
  <tr>
   <th>Branch</th>
  </tr>
 </thead>
 <tbody>
% for item in data['branches']:
  <tr>
   <td>{{item}}</td>
  </tr>
% end
 </tbody>
</table>

<h2>Configured servers</h2>

<table class="table table-condensed">
 <thead>
  <tr>
   <th>Alias</th>
   <th>Hostname</th>
   <th>Directory</th>
   <th>Username</th>
   <th>Branch</th>
  </tr>
 </thead>
 <tbody>
% for item in data['servers']:
  <tr>
   <td>{{item['alias']}}</td>
   <td>{{item['hostname']}}</td>
   <td>{{item['directory']}}</td>
   <td>{{item['username']}}</td>
   <td>{{item['branch']}}</td>
  </tr>
% end
 </tbody>
</table>

