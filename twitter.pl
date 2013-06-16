#!/usr/bin/perl -w

#####################################
#   query must be done like this:   #
#   twitter.pl?do=open              #
#   twitter.pl?do=close             #
#   twitter.pl?do=custom&hours=x    #
#   twitter.pl?request              #
#####################################

use Net::Twitter;
use POSIX qw(strftime);
use CGI qw(:standard);
print "Content-Type: text/html", "\n\n";

sub Usage {
    print "<pre>USAGE:
    ?do=close           Close the space,
    ?do=open            Open the space,
    ?do=custom&hours=x  Open the space for a specific time,
    ?request            Request the state of the hackerspace (open/closed).</pre>\n";
    exit();
}

# IP check
my $ip = $ENV{'REMOTE_ADDR'};
if($ip !~ /^62\.220\.13\d\.\d{1,3}/ && $ip !~ /^2001:788:dead:beef/) {
  print "This script is only accessible from within the hackerspace, sorry!<br/><br/>\n\nVisit <a href=\"https://fixme.ch\">fixme.ch</a> for more information. <br/><br/><small>" . $ENV{'REMOTE_ADDR'} . "</small>" ;
  exit();
}

# Twitter OAuth
my $client = Net::Twitter->new(
  #traits          => [qw/OAuth API::REST/],
  traits          => [qw/API::RESTv1_1/],
  consumer_key    => "",
  consumer_secret => "",
  access_token    => "",
  access_token_secret => "",
);

# Authorize
#print "Authorize this app at ", $client->get_authorization_url, " and hit RET\n";
#my $pin = <STDIN>;
#chomp $pin;
#my($access_token, $access_token_secret) = $client->request_access_token(verifier => $pin);
#print "access token=", $access_token, "\n";
#print "access token secret=", $access_token_secret, "\n";

# Parse GET data & create status
my $status;
my $date = strftime "%d.%m.%Y %H:%M", localtime;
if(param("do")) {
  my $do = param("do");
  if ($do =~ m/^open$/) {
    rename("closed", "open");
    $status ="The space is now open, you are welcome to come over! (" . $date . ")";
  }
  elsif($do =~ m/^close[d]{0,1}$/) {
    rename("open", "closed");
    $status = "The space is now closed, see you later! (" . $date . ")";
  }
  elsif($do =~ m/^custom$/ && param("hours") || $do =~ m/^open$/ && param("hours") ) {
    rename("closed", "open");
    my $hours = param("hours");
    $status = "The space is open for approx. " . $hours . "h, you are welcome to come over! (" . $date . ")";
  }
  else {
    &Usage();
  }
} elsif (param("request")) {
   if (-e "open") {
       print "The hackerspace seems to be open<br/>\n";
   } elsif (-e "closed") {
      print "The hackerspace seems to be closed<br/>\n"
   } else {
       print "No information on the state of the hackerspace<br/>\n";
   }
   exit();
} else {
    &Usage();
} 

# Post status
if($client->authorized){
  print "updating status ... <br/>\n";
  my $ret = $client->update({status => $status});
  if ($ret == undef){
    print $client->get_error();
  }
  else {
    print $status;
  }
}else{
  print "Client is not authorized anymore!";
}

# Post Hackerspace status on website
use DBI();

$host = "";
$database = "";
$tablename = "";
$user = "";
$pw = "";
$table = "";

$dsn = "DBI:mysql:database=$database;host=$host";
$con = DBI->connect($dsn, $user, $pw);

my $query;
if (param("do")) {
  my $do=param("do");
  my $pub_date = strftime "%Y-%m-%d %H:%M:%S", localtime;
  if ($do =~ m/^open$/) {
      $query = "INSERT INTO ". $table ." (pub_date, duration, open) VALUES ('". $pub_date ."', 0, 1)";
  }
  elsif($do =~ m/^close[d]{0,1}$/) {
      $query = "INSERT INTO ". $table ." (pub_date, duration, open) VALUES ('". $pub_date ."', 0, 0)";
  }
  elsif($do =~ m/^custom$/ && param("hours")) {
      $hours = param("hours");
      $query = "INSERT INTO ". $table ." (pub_date, duration, open) VALUES ('" . $pub_date . "', " . $hours . ", 1)";
  }

  if ($query) {
    $execute = $con->do($query);
  }
}
$con->disconnect();
