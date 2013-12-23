<div>
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

    </form>

</div>

<a onclick="$('#raw-data').show()">Show raw data</a>
<pre id="raw-data" style="display: none">{{data['raw']}}</pre>
