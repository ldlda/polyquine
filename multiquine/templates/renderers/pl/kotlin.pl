# LDA_REQUIRES: json
$RENDERERS->{'kotlin'} = sub { join('\\$', split(/\$/, $RENDERERS->{'json'}->($_[0]), -1)) };
