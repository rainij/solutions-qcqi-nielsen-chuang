# This is just some random program:
comments_and_indentation = dict(
    source="""# Anything behind '#' is a comment. Empty lines are ignored.

(S,■,2,X,+)  # We use "+" and "-" as shortcuts for +1 and -1.
  (2,■,3,Y,+)  # Indentation is irrelevant.
(3,■,H1,Z,-)  # We go to the left before halting - just for fun
(H1,Y,H,Y,0)
# whitespace inside (...) is (mostly) important. We could not replace the last line by this:
# (H1,Y,H ,Y,0)
""",
    parsed=[
        ('S', '■', '2', 'X', +1),
        ('2', '■', '3', 'Y', +1),
        ('3', '■', 'H1', 'Z', -1),
        ('H1', 'Y', 'H', 'Y', 0)
    ],
    source_map=[
        (2, "(S,■,2,X,+)  # We use \"+\" and \"-\" as shortcuts for +1 and -1."),
        (3, "  (2,■,3,Y,+)  # Indentation is irrelevant."),
        (4, "(3,■,H1,Z,-)  # We go to the left before halting - just for fun"),
        (5, "(H1,Y,H,Y,0)")
    ]
)
