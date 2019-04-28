
Welcome to the Pyalchemist package!
===================================

This is a very simple example package used as part of the UCL
[Research Software Engineering with Python](development.rc.ucl.ac.uk/training/engineering) course.

The package simulates Merlin's lab using instructions from his helper Daithi.


Installation:

Ready to go in no-time: "cd" into the package top-directory then run "pip install ."
The package can then be run anywhere on your machine. Simply use the command-line 
interface (entry-point) called "abracadabra". With "abracadabra -h" you will see a help
message from the package.
 

Usage:

Works in comand line only, after "cd" into the directory where your <yaml_file> lives. Then
invoke the tool with 'abracadabra <yaml_file>' to simulate interactions between your substances. 
There is also an optional flag '--reactions' run with 'abracadabra <yaml_file> --reactions'
that will only display the number of reactions that took place.


Output:

The output of 'abracadabra <yaml_file>' is in the form of:
'lower: [<list with substances remaining on lower shelf>]
 upper: [<list with substances remaining on upper shelf>]'
The output of 'abracadabra <yaml_file> --reactions' is in the form of:
'integer' (which is the number of reactions)


Example:

The yaml_file must define a 2-shelf standard laboratory, for example an example.yaml file may contain:
lower:[a, b, antia, d]
upper: [antia, b, antiantiantid, k]
The output of 'abracadabra example.yaml' will be:
lower:[b, antia]
upper:[b, k]
The output of 'abracadabra example.yaml --reactions' will be:
2


Notes:

1. The upper shelf 'anti' substances must begin with at least an 'anti' 
   e.g. transform '<Substanceanti>' to '<antiSubstance>'
2. Modify the Substance class from the 17032444\alchemist\laboratory.py
   file to create your own types of reactions! There is a Substance class pre-defined,
   but your are free to modify/build on it as you wish.
3. If you define a Substance class outside of the laboratory.py file, simply import it
   at the top of the file and delete the existing class. But this must be compatible
   with the Laboratory class and your can_react() method must return a boolean. If you're
   not sure, run the package with your class - there is a check inside Laboratory which will
   warn you.
4. In the existing Substance class, there is a reaction_type variable which can be modified.
   For example, 'over' can be used as a keyword instead of 'anti' e.g. 'involucrata' can be 
   made to react with 'overinvolucrata' or 'overoveroverinvolucrata'
5. In the existing Substance class, 'anti' substances can be defined with many 'anti' keywords.
   An even number of 'anti' will return the original substance e.g. 'antiantiSubstance'
   is transformed to 'Substance' while an odd number of 'anti' keywords returns 'antiSubstance'.
6. Some (possibly) missing dependencies will be installed: pyyaml and argparse. Without these,
   the package cannot run!

