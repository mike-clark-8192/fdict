import pcre2

# This regex matches dict literals that have only string-literal keys, and where the
# value assigned to said key comes from a variable name that matches the key name exactly.
# Examples: {"var1": var1}   /   {"var1": var1, "var2": var2}
DRY_RE_STR = r"""\{ # match opening brace
# match the first key-value pair and save the subpattern as 'expr'
(?P<expr>\s{0,99}
    # match 'keyname' or "key_name", for example, and save the match to named group 'key'
    ['\"](?P<key>\w+)['\"]\s{0,99}
    # match the colon and then back-reference the key name as being the assigned varname
    :\s{0,99}(?P=key)\s{0,99}
) # end of subpattern 'expr'
(?:,(?&expr))* # match zero-to-many ,-separated `"key": key` pairs
\}"""  # match the closing brace
DRY_RE = pcre2.compile(DRY_RE_STR, pcre2.X)

# This regex matches dict literals that have only string-literal keys, and where the
# value assigned to said key comes from a "simple expression":
# Examples: {"var1": var1}   /  {"key3": valueholder.avalue, "key4": 3 }
NONDRY_RE_STR = r"""\{ # match opening brace
# match the first key-value pair and save the subpattern as 'expr'
(?P<expr>\s{0,99}
    # match 'keyname' or "key_name", for example
    ['\"]\w+['\"]\s{0,99}
    # match the colon and then len()>1 sequence of simple expression chars
    :\s{0,99}[^{},]{1,99}\s{0,99}
) # end of subpattern 'expr'
(?:,(?&expr))* # match zero-to-many ,-separated `"key": key` pairs
\s{0,99},?\s{0,99}\}"""  # match the closing brace
NONDRY_RE = pcre2.compile(NONDRY_RE_STR, pcre2.X)
