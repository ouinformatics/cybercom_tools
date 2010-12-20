#!/bin/bash 
# converts from fixed width to delimited with '|' 
sed 's/ \{1,10\}/|/g' 20100931-123D-output.365088132.txt > 20100930-123D-output.365088132.del
sed 's/ \{1,10\}/|/g' 20100930-123D-output.83442912.txt > 20100930-123D-output.83442912.del
