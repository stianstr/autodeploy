use POSIX;
use Irssi;
use Irssi::Irc;
use LWP::UserAgent;
#use HTML::TreeBuilder;
use JSON;
use Data::Dumper;
#use strict;

use vars qw($VERSION %IRSSI);

$VERSION = "1.0";
%IRSSI = (
	authors     => "Stian Strandem",
	contact     => "stian@strandem.net",
	name        => "autodeploy.pl",
	description => "AutoDeploy",
	license     => "",
	url         => "",
);

my $baseUrl   = 'http://127.0.0.1:8080';
my $authAdr   = '127.0.0.1:8080';
my $authRealm = 'private';
my %users     = (
    'some-nick'    => { 'username' => 'some-user', 'password' => 'some-password' }
);

my $myNick;
my $currentTarget;
my $currentServer;
my $currentUsername;
my $currentPassword;

sub reply {
	my ($message) = @_;
	$currentServer->command("MSG $currentTarget $message");
}

sub debug {
	my ($message) = @_;
	Irssi::print "DEBUG: $message"
}

sub parseCommand {
	my ($input) = @_;
	my $command;
	if ($input =~ m/^(!|$myNick[\.,:;]?[ ]?)deploy ?(.*)$/i) {
		$command = $2;
		if (!$command) {
			$command = 'help';
		}
		return $command;
	}
}

sub cmdHelp {
	reply('deploy help');
	reply('deploy check <branch> <server>');
	reply('deploy push <branch> <server>');
	reply('deploy merge <branch> <server>');
	reply('deploy servers');
	reply('deploy branches');
}

sub cmdListServers {
	reply("Servers and their branches:");
	my $data = callAutoDeploy("/servers");
	if (!$data) {
		return;
	}
    foreach my $item (@{$data}) {
        reply("* " . $item->{"alias"} . " - " . $item->{"branch"});
    }
}

sub cmdListBranches {
	reply("Active branches:");
	my $data = callAutoDeploy("/branches");
	if (!$data) {
		return;
	}
    foreach my $item (@{$data}) {
        reply("* " . $item);
    }
}

sub handleCheckResult {
    my ($action, $result) = @_;
    #debug("DUMP: " . Dumper($result));
    #debug("RES.result: " . $result->{ "result" });
    #debug("RES.server: " . $result->{ "server" });
    #debug("RES.branch: " . $result->{ "branch" });
    #debug("RES.c.lock: " . $result->{ "check" }->{ "lock" }->{ "result" });
    #debug("RES.c.merg: " . $result->{ "check" }->{ "merge" }->{ "result" });
    #debug("RES.c.ucom: " . $result->{ "check" }->{ "uncomitted" }->{ "result" });
    #debug("RES.c.buil: " . $result->{ "check" }->{ "build" }->{ "result" });
    if (!$result) {
        return;
    }
    if ($result->{ "result" }) {
        if ($action eq "check") {
            reply("[SUCCESS] Branch can be deployed");
        } else {
            reply("[SUCCESS] Branch was successfully deployed");
        }
    } else {
        reply("[FAIL] Branch cannot be deployed, because:");
        if (!$result->{ "check" }->{ "type" }->{ "result" }) {
            reply("* " . $result->{ "check" }->{ "type" }->{ "message" });
        }
        if (!$result->{ "check" }->{ "lock" }->{ "result" }) {
            reply("* " . $result->{ "check" }->{ "lock" }->{ "message" });
        }
        if (!$result->{ "check" }->{ "merge" }->{ "result" }) {
            reply("* " . $result->{ "check" }->{ "merge" }->{ "message" });
        }
        if (!$result->{ "check" }->{ "uncomitted" }->{ "result" }) {
            reply("* " . $result->{ "check" }->{ "uncomitted" }->{ "message" });
        }
        if (!$result->{ "check" }->{ "build" }->{ "result" }) {
            reply("* " . $result->{ "check" }->{ "build" }->{ "message" });
        }
    }
    my $url = $baseUrl . "?show=" . $result->{ "id" };
    reply("For details see: $url");
}

sub cmdCheck {
	my ($branch,$server) = @_;
	reply("[CHECK] if branch: $branch can be deployed to server: $server");
	my $result = callAutoDeploy("/check/$server/$branch");
    handleCheckResult("check", $result);
}

sub cmdPush {
	my ($branch,$server) = @_;
	reply("[PUSH] branch: $branch to server: $server");
	my $result = callAutoDeploy("/deploy/$server/$branch");
    handleCheckResult("push", $result);
}

sub cmdMerge {
	my ($branch,$server) = @_;
	reply("[MERGE] branch: $branch into master and switch server: $server");
	my $result = callAutoDeploy("/merge/$server/$branch");
    debug("RESULT: ".Dumper($result));
    if ($result && $result->{ "result" }) {
        reply("Successfully merged. Server $server is now back on master, and branch $branch is merged into master");
    } else {
        reply("Failed merging $branch into master: " . $result->{ "message" });
    }
}

sub handleInput {

	my ($server, $input, $userNick, $userMask, $target) = @_;
        $myNick          = $server->{'nick'};
	    $currentTarget   = $target;
		$currentServer   = $server;
        $currentUsername = '';
        $currentPassword = '';

	debug("nick: $userNick / input: $input / target: $target / mask: $userMask"); # tmp

	my $command = parseCommand($input);
    debug("cmd: $command");
	if ($command) {

		# HELP
		if ($command eq "help" || $command eq "") {
			cmdHelp();
			return;
        } else {

            $currentUsername = $users{ $userNick }{'username'};
            $currentPassword = $users{ $userNick }{'password'};

            if ($currentUsername) {

                # LIST SERVERS
                if ($command eq "servers") {
                    cmdListServers();
                    return;

                # LIST BRANCHES
                } elsif ($command eq "branches") {
                    cmdListBranches();
                    return;

                # DEPLOY
                } else {

                    # Parse params
                    my $type;
                    my $branch;
                    my $server;
                    my $valid   = 1;
                    my @parts   = split(/ /, $command);
                    my $partlen = $#parts+1;
                    if ($partlen eq 3) {
                        $type   = $parts[0];
                        $branch = $parts[1];
                        $server = $parts[2];
                        if ($type eq "check") {
                            cmdCheck($branch, $server);
                            return;
                        } elsif ($type eq "push") {
                            cmdPush($branch, $server);
                            return;
                        } elsif ($type eq "merge") {
                            cmdMerge($branch, $server);
                            return;
                        }
                    }

                }
            } else {
                reply("must configure your nick under users for this command");
                return;
            }

        }

		reply("invalid command - for help try: deploy help");
	}
}


sub callAutoDeploy {
	my ($url) = @_;
	$url = $baseUrl . $url;
	debug("UA.request: $url");

	my $userAgent = LWP::UserAgent->new();
    debug("username: $currentUsername");
    $userAgent->credentials($authAdr, $authRealm, $currentUsername, $currentPassword);

	$userAgent->timeout(60);
    $userAgent->default_header("Content-Type" => "application/json");
	my $response = $userAgent->get($url);
	if ($response->is_success) {
		debug("UA.response: " . $response->decoded_content);
		return decode_json($response->decoded_content);
	} else {
		debug("UA.response is ERROR: ".$response->status_line);
		reply("Failed talking to AutoDeploy: " . $response->status_line);
	}
}	

Irssi::signal_add_last("message public", "handleInput");
