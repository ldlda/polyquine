$RENDERERS->{'php'} = sub {
    my $s = $_[0];
    $s =~ s{\\}{\\\\}g;
    $s =~ s{'}{\\'}g;
    "'" . $s . "'"
};
