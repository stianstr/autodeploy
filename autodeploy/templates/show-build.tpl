<div class="row">

<div class="col-md-5">

    <h2>Info</h2>

    <form class="form-horizontal" role="form">

    <div class="form-group">
        <label class="col-xs-2 control-label">Status</label>
        <div class="col-xs-10">
        <p class="form-control-static status-value">
            % if data['result']:
                <span class="label label-success">success</span>
            % else:
                <span class="label label-danger">fail</span>
            % end
        </p>
        </div>
    </div>

    <div class="form-group">
        <label class="col-xs-2 control-label">Branch</label>
        <div class="col-xs-10">
            <p class="form-control-static branch-value">
                <span class="label label-info">{{data['branch']}}</label>
            </p>
        </div>
    </div>

    <div class="form-group">
        <label class="col-xs-2 control-label">Server</label>
        <div class="col-xs-10">
            <p class="form-control-static">{{data['server']}}</p>
        </div>
    </div>

    <div class="form-group">
        <label class="col-xs-2 control-label">User</label>
        <div class="col-xs-10">
            <p class="form-control-static">{{data['user']}}</p>
        </div>
    </div>

    <div class="form-group">
        <label class="col-xs-2 control-label">Time</label>
        <div class="col-xs-10">
            <p class="form-control-static">{{data['time']}}</p>
        </div>
    </div>

<!--
    <div class="form-group">
        <label class="col-xs-2 control-label">Revision</label>
        <div class="col-xs-10">
            <p class="form-control-static">{{data['check']['revision']}}</p>
        </div>
    </div>

    <div class="form-group">
        <label class="col-xs-2 control-label">ID</label>
        <div class="col-xs-10">
            <p class="form-control-static">{{data['id']}}</p>
        </div>
    </div>
-->

    </form>

</div>

<div class="col-md-7">

    <h2>Checklist</h2>

    <ul class="checklist">

    % if data['check']['type']['result']:
    <li class="ok">
    <i class="glyphicon glyphicon-ok"></i>
    Branch should be of correct type
    % else:
    <li class="error">
    <i class="glyphicon glyphicon-remove"></i>
    Branch should be of correct type
    <div class="checklist-check alert alert-danger">
    {{data['check']['type']['message']}}
    </div>
    % end
    </li>

    % if data['check']['build']['result']:
    <li class="ok">
    <i class="glyphicon glyphicon-ok"></i>
    Build status should be green
    % else:
    <li class="error">
    <i class="glyphicon glyphicon-remove"></i>
    Build status should be green
    <div class="checklist-check alert alert-danger">
    {{data['check']['build']['message']}}
    % if data['check']['build']['buildLink']:
        - <a href="{{data['check']['build']['buildLink']}}">View build</a>
    % end
    </div>
    % end
    </li>

    % if data['check']['uncomitted']['result']:
    <li class="ok">
    <i class="glyphicon glyphicon-ok"></i>
    Server should not have uncomitted changes
    % else:
    <li class="error">
    <i class="glyphicon glyphicon-remove"></i>
    Server should not have uncomitted changes
    <div class="checklist-check alert alert-danger">
    {{data['check']['uncomitted']['message']}}:
    <pre>{{data['check']['uncomitted']['changes']}}</pre>
    <div><a onclick="autoDeploy.openHelpDialog('uncomitted-changes')">Help</a></div>
    </div>
    % end
    </li>

    % if data['check']['merge']['result']:
    <li class="ok">
    <i class="glyphicon glyphicon-ok"></i>
    Branch should contain master
    % else:
    <li class="error">
    <i class="glyphicon glyphicon-remove"></i>
    Branch should contain master
    <div class="checklist-check alert alert-danger">
    {{data['check']['merge']['message']}}
    <div><a onclick="autoDeploy.openHelpDialog('master-in-branch')">Help</a></div>
    </div>
    % end
    </li>

    % if data['check']['lock']['result']:
    <li class="ok">
    <i class="glyphicon glyphicon-ok"></i>
    Server should not already be staging
    % else:
    <li class="error">
    <i class="glyphicon glyphicon-remove"></i>
    Server should not already be staging
    <div class="checklist-check alert alert-danger">
    {{data['check']['lock']['message']}}
    <div><a onclick="autoDeploy.openHelpDialog('already-staging')">Help</a></div>
    </div>
    % end
    </li>

    </ul>

</div>

</div>

<a onclick="$('#raw-data').show()">Show raw data</a>
<pre id="raw-data" style="display: none">{{data['raw']}}</pre>
