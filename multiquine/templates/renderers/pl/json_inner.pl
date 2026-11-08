# LDA_REQUIRES: json
$RENDERERS->{'json_inner'} = sub { substr($RENDERERS->{'json'}->($_[0]), 1, -1) };
