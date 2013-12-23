var AutoDeploy = function() {
    var self = this;

    self.openShowDialog = function(id) {
        var url = '/show/' + id + '?headless=1';
        $('#showModal').modal('show');
        $('#showModal .modal-body').html('Loading...');
        $('#showModal .modal-body').load(url);
    }

    self.openHelpDialog = function(topic) {
        var url = '/help/' + topic + '?headless=1';
        $('#helpModal').modal('show');
        $('#helpModal .modal-body').html('Loading...');
        $('#helpModal .modal-body').load(url);
    }

}
