$RENDERERS->{'json'} = sub {
    my $quoted = JSON::PP->new->ascii->allow_nonref->encode($_[0]);
    $quoted =~ s{\x7f}{\\u007f}g;
    return $quoted;
};
