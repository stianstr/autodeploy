% if not data['headless']:
    % include templates/header
% end

% if not data['headless']:
    <div class="main-container">
% end

% if data['type'] == 'merge':
    % include templates/show-merge data=data
% else:
    % include templates/show-build data=data
% end

% if not data['headless']:
    </div>
% end

% if not data['headless']:
    % include templates/footer
% end
