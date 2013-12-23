% include templates/header

<header>
  <h3>Auto-deploy</h3>

  <!-- Nav tabs -->
  <ul class="nav nav-tabs">
    <li clasS="active"><a href="#front" data-toggle="tab">Front</a></li>
    <li><a href="#procedure" data-toggle="tab">Procedure</a></li>
    <li><a href="#api" data-toggle="tab">API</a></li>
  </ul>
</header>

<!-- Tab panes -->
<div class="tab-content">
  <div class="tab-pane active" id="front">
  % include templates/front data=data
  </div>
  <div class="tab-pane" id="procedure">
  % include templates/procedure
  </div>
  <div class="tab-pane" id="api">
  % include templates/api
  </div>
</div>

<!-- Modal -->
<div class="modal fade" id="showModal" tabindex="-1" role="dialog" aria-labelledby="showModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
<!--
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="showModalLabel">Details</h4>
      </div>
-->
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
<!--
        <button type="button" class="btn btn-primary">Save changes</button>
-->
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

<!-- Modal -->
<div class="modal fade" id="helpModal" tabindex="-1" role="dialog" aria-labelledby="helpModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
<!--
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="helpModalLabel">Details</h4>
      </div>
-->
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
<!--
        <button type="button" class="btn btn-primary">Save changes</button>
-->
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->

% include templates/footer

<script type="text/javascript">
var autoDeploy = new AutoDeploy();
% if data['showDetails']:
    autoDeploy.openShowDialog('{{data['showDetails']}}');
% end
</script>
