# User-provided Element451 function training source

This file preserves the function training material supplied by the skill author. Treat it as a bundled working reference, not as proof of current product behavior. Tenant prefixes and numeric identifiers in examples have been generalized to fictional `school.*` values; they demonstrate mapping direction only and must never be treated as valid tenant configuration. Preserve the source terminology and note its internal duplicates or discrepancies rather than silently reconciling them. Consult `formula-functions.md` for the curated catalog and verify current behavior against official Element451 documentation when needed.

## Table of contents

- [1. IF](#1-if)
- [2. REGEXP_MATCH](#2-regexpmatch)
- [3. REGEXP_EXTRACT](#3-regexpextract)
- [4. REGEXP_EXTRACT_NTH](#4-regexpextractnth)
- [5. CEEB_MAP](#5-ceebmap)
- [6. DS_MAP](#6-dsmap)
- [7. TAXONOMY_MAP](#7-taxonomymap)
- [8. CHECKBOX_CHECKED](#8-checkboxchecked)
- [9. DB_MAP](#9-dbmap)
- [10. SC_MAP_IMPORT](#10-scmapimport)
- [11. SC_MAP_EXPORT](#11-scmapexport)
- [12. DATE_ADD](#12-dateadd)
- [13. DATE_DIFF](#13-datediff)
- [14. DATE_COMPARE](#14-datecompare)
- [15. DATE_FORMAT](#15-dateformat)
- [16. DATE_DEFAULT](#16-datedefault)
- [17. DATE_READ](#17-dateread)
- [18. SQR](#18-sqr)
- [19. SIN](#19-sin)
- [20. ATAN](#20-atan)
- [21. COSH](#21-cosh)
- [22. COTAN](#22-cotan)
- [23. EXP](#23-exp)
- [24. LN](#24-ln)
- [25. LOG](#25-log)
- [26. SQRT](#26-sqrt)
- [27. ABS](#27-abs)
- [28. SIGN](#28-sign)
- [29. TRUNC](#29-trunc)
- [30. CEIL](#30-ceil)
- [31. FLOOR](#31-floor)
- [32. RND](#32-rnd)
- [33. VAL](#33-val)
- [34. POW](#34-pow)
- [35. MIN](#35-min)
- [36. MAX](#36-max)
- [37. MOD](#37-mod)
- [38. NUM](#38-num)
- [39. SUM](#39-sum)
- [40. DATE_FORMAT](#40-dateformat)
- [41. DATE_ADD](#41-dateadd)
- [42. DB_MAP](#42-dbmap)
- [43. Default Literal](#43-default-literal)
- [44. DS_MAP](#44-dsmap)
- [45. DS_MAP (Nested)](#45-dsmap-nested)
- [46. IF](#46-if)
- [47. IF + DATE_DIFF + DATE_FORMAT](#47-if-datediff-dateformat)
- [48. SPLIT_INDEX](#48-splitindex)
- [49. ZIPCODE SUBSTR+IF+STRLEN+PAD](#49-zipcode-substrifstrlenpad)
- [50. TAXONOMY_MAP](#50-taxonomymap)
- [51. REGEX_REPLACE](#51-regexreplace)
- [52. CHECKBOX_FIRST](#52-checkboxfirst)
- [53. CONTAINS](#53-contains)
- [54. HAS_ONE_TRUE](#54-hasonetrue)
- [55. STARTS_WITH](#55-startswith)
- [56. ENDS_WITH](#56-endswith)

---

1. IF
Signature
IF(b, case1, case2)


Function Type
 Logic
Description
 The IF(b, case1, case2) function provides branching capability.
* If b is not 0, it returns case1; otherwise it returns case2.

* Behavior is similar to PHP’s b ? case1 : case2.

* When b == 0, case1 will not be evaluated (and vice‑versa).

* Supports logical operators “and”, “or”, and “not” using &, |, and !.

Common Usage Examples
Expression
	Meaning
	IF([C1] <> [C2], [C3], "Failed")
	Check if two cells are not equal.
	IF([C1] = [C2], [C3], "Failed")
	Check if two cells are equal.
	IF([C1] = "Y" & [C2] = "Y", [C3], "Failed")
	Check if both cells are true.
	IF([C1] = "Y" | [C2] = "Y", [C3], "Failed")
	Check if either cell is true.
	IF(![C1] = "Y", [C3], "Failed")
	Apply not: flips true⇄false on the test.
	Parameter Summary
   * Name: IF

   * Number of parameters: 3

   * Parameter types: bool, any, any

Example input:

 IF(HEIGHT, 3/HEIGHT, 3)  
      *       * Example description:
 Ensures 3/HEIGHT does not cause division by zero.

________________


2. REGEXP_MATCH
Signature
REGEXP_MATCH(text, pattern)


Function Type
 Regex Operations
Description
 Matches an entire string against a PHP‐style regular expression. Returns TRUE if the pattern matches, FALSE otherwise.
Example
INPUT:  REGEXP_MATCH("Hello World", "H[a-z]{4}\s.*")  
OUTPUT: TRUE  


Parameter Summary
         * Name: REGEXP_MATCH

         * Number of parameters: 2

         * Parameter types: string, pattern

         * Example input/output:

            * REGEXP_MATCH("Hello World", "H[a-z]{4}\s.*") → TRUE

________________


3. REGEXP_EXTRACT
Signature
REGEXP_EXTRACT(text, pattern)


Function Type
 Regex Operations
Description
 Extracts and returns the substring that matches the first parenthetical capture group in the given PHP‐style regular expression.
Example
INPUT:  REGEXP_EXTRACT("Hello World", "Hello\s(.*)")  
OUTPUT: "World"  


Parameter Summary
               * Name: REGEXP_EXTRACT

               * Number of parameters: 2

               * Parameter types: string, pattern

               * Example input/output:

                  * REGEXP_EXTRACT("Hello World", "Hello\s(.*)") → "World"

________________


4. REGEXP_EXTRACT_NTH
Signature
REGEXP_EXTRACT_NTH(text, pattern, n)


Function Type
 Regex Operations
Description
 Extracts and returns the substring that matches the nth parenthetical capture group in the given PHP‐style regular expression.
Example
INPUT:  REGEXP_EXTRACT_NTH("Hello World", "H([a-z]+)\s(.*)", 1)  
OUTPUT: "ello"  


Parameter Summary
                     * Name: REGEXP_EXTRACT_NTH

                     * Number of parameters: 3

                     * Parameter types: string, pattern, index

                     * Example input/output:

                        * REGEXP_EXTRACT_NTH("Hello World", "H([a-z]+)\s(.*)", 1) → "ello"

________________


5. CEEB_MAP
Signature
CEEB_MAP(input, match_key, output_key, default)


Function Type
 Maps and Lists
Description
 Identical to DS_MAP, but uses the luminous_ceebs collection as its data source.
Looks up the record where match_key == input and returns that record’s output_key field; if no match is found, returns default.
Example
INPUT:  CEEB_MAP(181615, "ceeb", "name", "CeebNotFound")  
OUTPUT: "Academy At Shawnee"  


Parameter Summary
                           * Name: CEEB_MAP

                           * Number of parameters: 4

                           * Parameter types: input, match, output, default

                           * Example input/output:

                              * CEEB_MAP(181615, "ceeb", "name", "CeebNotFound") → "Academy At Shawnee"

________________


6. DS_MAP
Signature
DS_MAP(input, dataSource, match_key, output_key, default)


Function Type
 Maps and Lists
Description
 General “data‐source” mapping function.
                                 1. Look up the luminous_data_sources collection for the given dataSource.

                                 2. Within that object’s options array, find the entry where match_key == input.

                                 3. Return that entry’s output_key field.

                                 4. If no entry matches, return default.

Examples
INPUT:  DS_MAP("school.terms.41001",   "data_source.terms",   "guid",   "name", "TermNotFound")  
OUTPUT: "Fall 2016"  


INPUT:  DS_MAP("school.terms.41350","data_source.terms",   "guid",   "name", "TermNotFound")  
OUTPUT: "TermNotFound"  


INPUT:  DS_MAP("USA",           "data_source.country", "alpha3", "name", "CountryNotFound")  
OUTPUT: "United States"  


Parameter Summary
                                    * Name: DS_MAP

                                    * Number of parameters: 5

                                    * Parameter types: input, dataSource, match, output, default

                                    * Example input/output:
                                       * as shown above

________________


7. TAXONOMY_MAP
Signature
TAXONOMY_MAP(input, match_key, output_key, default)


Function Type
 Maps and Lists
Description
 Fetches an entry from a taxonomy.
                                          1. Look up the luminous_taxonomies collection for items.

                                          2. Find the entry where match_key == input.

                                          3. Return that entry’s output_key field.

                                          4. If no entry matches, return default.

Examples
INPUT:  TAXONOMY_MAP("school.taxonomy.51018", "guid",  "value",  "MISSING")  
OUTPUT: "grad-admit"  


INPUT:  TAXONOMY_MAP("school.taxonomy.51018", "guid",  "name",   "MISSING")  
OUTPUT: "Grad Admits"  


INPUT:  TAXONOMY_MAP("",                "guid",  "name",   "MISSING")  
OUTPUT: "MISSING"  


INPUT:  TAXONOMY_MAP("grad-admit",     "value", "name",   "MISSING")  
OUTPUT: "Grad Admits"  


INPUT:  TAXONOMY_MAP("grad-admit",     "value", "guid",   "MISSING")  
OUTPUT: "school.taxonomy.51006"  


Parameter Summary
                                             * Name: TAXONOMY_MAP

                                             * Number of parameters: 4

                                             * Parameter types: input, match_key, output_key, default

________________


8. CHECKBOX_CHECKED
Signature
CHECKBOX_CHECKED(json_input, delimiter)


Function Type
 Maps and Lists
Description
 Parses a JSON‑style array of objects, each with fields checked (boolean) and text (string).
Concatenates the text values for all objects where checked == TRUE, separated by the specified delimiter.
Examples
INPUT:  CHECKBOX_CHECKED(
  "[{'checked':true,'text':'Asian'},
    {'checked':false,'text':'European'},
    {'checked':true,'text':'American'}]",
  ","
)
OUTPUT: "Asian,American"  


INPUT:  CHECKBOX_CHECKED(
  "[{'checked':false,'text':'Asian'},
    {'checked':false,'text':'European'},
    {'checked':false,'text':'American'}]",
  ","
)
OUTPUT: ""  


Parameter Summary
                                                * Name: CHECKBOX_CHECKED

                                                * Number of parameters: 2

                                                * Parameter types: json_input, delimiter

________________


9. DB_MAP
Signature
DB_MAP(type, input, match_key, output_key, default)


Function Type
 Maps and Lists
Description
 Universal database mapper for internal usage.
                                                   * Internally used by TAXONOMY_MAP, SC_MAP_IMPORT, and SC_MAP_EXPORT.

                                                   * Trims whitespace from input and replaces all non‑alphanumeric characters with _ before matching.

                                                   * Searches the specified type (e.g., "term", "major", "taxonomy") collection.

Example
INPUT:  DB_MAP(
  "taxonomy", 
  "grad-admit", 
  "value", 
  "guid", 
  "MISSING"
)
OUTPUT: "school.taxonomy.51006"  


Parameter Summary
                                                      * Name: DB_MAP

                                                      * Number of parameters: 5

                                                      * Parameter types: type, input, match_key, output_key, default

________________


10. SC_MAP_IMPORT
Signature
SC_MAP_IMPORT(input, default)


Function Type
 Maps and Lists
Description
 Alias for importing a user’s taxonomy selection.
                                                         * Uses TAXONOMY_MAP under the hood with match_key="value" and output_key="guid".

                                                         * Intended for [user-sources-source-code] and [user-sources-source-code-segment] fields.

Example
INPUT:  SC_MAP_IMPORT([C42], "MISSING")  
ALIAS FOR: TAXONOMY_MAP([C42], "value", "guid", "MISSING")  
OUTPUT: "school.taxonomy.52001"  


Parameter Summary
                                                            * Name: SC_MAP_IMPORT

                                                            * Number of parameters: 2

                                                            * Parameter types: input, default

________________


11. SC_MAP_EXPORT
Signature
SC_MAP_EXPORT(input, default)


Function Type
 Maps and Lists
Description
 Alias for exporting a user’s taxonomy selection.
                                                               * Uses TAXONOMY_MAP under the hood with match_key="guid" and output_key="value".

                                                               * Intended for [user-custom-field-source] fields.

Example
INPUT:  SC_MAP_EXPORT([user-custom-field-source], "MISSING")  
ALIAS FOR: TAXONOMY_MAP([user-custom-field-source], "guid", "value", "MISSING")  
OUTPUT: "grad-admit"  


Parameter Summary
                                                                  * Name: SC_MAP_EXPORT

                                                                  * Number of parameters: 2

                                                                  * Parameter types: input, default

________________


12. DATE_ADD
Signature
DATE_ADD(datePart, interval, date)


Function Type
 Date Functions
Description
 Adds an integer interval of a given datePart to a date.
                                                                     * datePart may be one of: second, minute, hour, day, month, year.

                                                                     * date must be in Y-m-d H:i:s format.

                                                                     * Returns a new date in the same format.

Example
INPUT:  DATE_ADD("month", 5, "2016-10-04 12:45:23")  
OUTPUT: "2017-03-04 12:45:23"  


Parameter Summary
                                                                        * Name: DATE_ADD

                                                                        * Number of parameters: 3

                                                                        * Parameter types: datePart, interval, date

________________


13. DATE_DIFF
Signature
DATE_DIFF(datePart, startDate, endDate)


Function Type
 Date Functions
Description
 Calculates the difference between endDate and startDate in the specified datePart.
                                                                           * datePart may be one of: second, minute, hour, day, month, year.

                                                                           * Dates must be in Y-m-d H:i:s format.

                                                                           * Returns an integer.

Example
INPUT:  DATE_DIFF(
  "month",
  "2016-10-04 12:45:23",
  "2017-03-04 12:45:23"
)
OUTPUT: 5  


Parameter Summary
                                                                              * Name: DATE_DIFF

                                                                              * Number of parameters: 3

                                                                              * Parameter types: datePart, startDate, endDate

________________


14. DATE_COMPARE
Signature
DATE_COMPARE(p1, operator, p2)


Function Type
 Date Functions
Description
 Compares two dates using the specified operator.
                                                                                 * p1 and p2 must be in Y-m-d H:i:s format.

                                                                                 * operator may be one of: <>, <, <=, >=, !=, =.

                                                                                 * Returns TRUE if the comparison holds, FALSE otherwise.

Example
INPUT:  DATE_COMPARE(
  "2016-10-04 12:45:23",
  "=",
  "2016-10-04 12:45:23"
)
OUTPUT: TRUE  


Parameter Summary
                                                                                    * Name: DATE_COMPARE

                                                                                    * Number of parameters: 3

                                                                                    * Parameter types: p1, operator, p2

________________


15. DATE_FORMAT
Signature
DATE_FORMAT(inputDate, format)


Function Type
 Date Functions
Description
 Reformats the given inputDate (in Y-m-d H:i:s format) according to the specified PHP‐style format string.
Example
INPUT:  DATE_FORMAT("2016-10-04 12:45:23", "D M d H:i:s O Y")  
OUTPUT: Tue Oct 04 12:45:23 +0000 2016  


Parameter Summary
                                                                                       * Name: DATE_FORMAT

                                                                                       * Number of parameters: 2

                                                                                       * Parameter types: inputDate, format

________________


16. DATE_DEFAULT
Signature
DATE_DEFAULT(format)


Function Type
 Date Functions
Description
 Formats the current date/time according to the specified PHP‐style format string.
Example
INPUT:  DATE_DEFAULT("D M d H:i:s O Y")  
OUTPUT: Fri Nov 17 09:29:26 -0500 2017  


Parameter Summary
                                                                                          * Name: DATE_DEFAULT

                                                                                          * Number of parameters: 1

                                                                                          * Parameter types: format

________________


17. DATE_READ
Signature
DATE_READ(dateString, format)


Function Type
 Date Functions
Description
 Parses an arbitrarily formatted dateString according to the given format (PHP‐style), and converts it to the standard Y-m-d H:i:s format.
Example
INPUT:  DATE_READ("01/02/03", "d/m/y")  
OUTPUT: 2003-02-01 00:00:00  


Parameter Summary
                                                                                             * Name: DATE_READ

                                                                                             * Number of parameters: 2

                                                                                             * Parameter types: dateString, format

________________


18. SQR
Signature
SQR(x)


Function Type
 Math Functions
Description
 Returns the square of x (i.e. x2x^2).
Example
INPUT:  SQR(451)  
OUTPUT: 203401  


Parameter Summary
                                                                                                * Name: SQR

                                                                                                * Number of parameters: 1

                                                                                                * Parameter types: number

________________


19. SIN
Signature
SIN(x)


Function Type
 Math Functions
Description
 Returns the sine of the angle x (in radians).
Example
INPUT:  SIN(1)  
OUTPUT: 0.84{...}  


Parameter Summary
                                                                                                   * Name: SIN

                                                                                                   * Number of parameters: 1

                                                                                                   * Parameter types: number

________________


20. ATAN
Signature
ATAN(x)


Function Type
 Math Functions
Description
 Returns the inverse tangent (arctangent) of x.
Example
INPUT:  ATAN(1)  
OUTPUT: 0.79{...}  


Parameter Summary
                                                                                                      * Name: ATAN

                                                                                                      * Number of parameters: 1

                                                                                                      * Parameter types: number

________________


21. COSH
Signature
COSH(x)


Function Type
 Math Functions
Description
 Returns the hyperbolic cosine of x.
Example
INPUT:  COSH(1)  
OUTPUT: 1.54{...}  


Parameter Summary
                                                                                                         * Name: COSH

                                                                                                         * Number of parameters: 1

                                                                                                         * Parameter types: number

________________


22. COTAN
Signature
COTAN(x)


Function Type
 Math Functions
Description
 Returns the cotangent of x (i.e. cos⁡xsin⁡x\frac{\cos x}{\sin x}).
Example
INPUT:  COTAN(1)  
OUTPUT: 0.64{...}  


Parameter Summary
                                                                                                            * Name: COTAN

                                                                                                            * Number of parameters: 1

                                                                                                            * Parameter types: number

________________


23. EXP
Signature
EXP(x)


Function Type
 Math Functions
Description
 The exponential function EXP(X) returns eXe^X, where e≈2.71828e\approx2.71828.
Example
INPUT:  EXP(1)  
OUTPUT: 2.72{...}  


Parameter Summary
                                                                                                               * Name: EXP

                                                                                                               * Number of parameters: 1

                                                                                                               * Parameter types: number

________________


24. LN
Signature
LN(x)


Function Type
 Math Functions
Description
 The natural logarithm function LN(X) returns the logarithm of X to base ee (where e≈2.71828e\approx2.71828).
Example
INPUT:  LN(451)  
OUTPUT: 6.11{...}  


Parameter Summary
                                                                                                                  * Name: LN

                                                                                                                  * Number of parameters: 1

                                                                                                                  * Parameter types: number

________________


25. LOG
Signature
LOG(x)


Function Type
 Math Functions
Description
 Returns the common (base‑10) logarithm of X.
Example
INPUT:  LOG(451)  
OUTPUT: 2.65{...}  


Parameter Summary
                                                                                                                     * Name: LOG

                                                                                                                     * Number of parameters: 1

                                                                                                                     * Parameter types: number

________________


26. SQRT
Signature
SQRT(x)


Function Type
 Math Functions
Description
 Returns the (principal) square root of X, i.e. the number R such that R2=XR^2 = X.
Example
INPUT:  SQRT(203401)  
OUTPUT: 451  


Parameter Summary
                                                                                                                        * Name: SQRT

                                                                                                                        * Number of parameters: 1

                                                                                                                        * Parameter types: number

________________


27. ABS
Signature
ABS(x)


Function Type
 Math Functions
Description
 Returns the absolute value of X, denoted ∣X∣\lvert X\rvert.
Example
INPUT:  ABS(-451)  
OUTPUT: 451  


Parameter Summary
                                                                                                                           * Name: ABS

                                                                                                                           * Number of parameters: 1

                                                                                                                           * Parameter types: number

________________


28. SIGN
Signature
SIGN(x)


Function Type
 Math Functions
Description
 Returns the sign of X:
                                                                                                                              * -1 if X < 0

                                                                                                                              * 0 if X = 0

                                                                                                                              * +1 if X > 0

Examples
INPUT:  SIGN(451)  
OUTPUT:  1  


INPUT:  SIGN(-451)  
OUTPUT: -1  


Parameter Summary
                                                                                                                                 * Name: SIGN

                                                                                                                                 * Number of parameters: 1

                                                                                                                                 * Parameter types: number

________________


29. TRUNC
Signature
TRUNC(x)


Function Type
 Math Functions
Description
 Truncates X by discarding its fractional part:
                                                                                                                                    * For positive X, equivalent to FLOOR(X)

                                                                                                                                    * For negative X, equivalent to CEIL(X)

Examples
INPUT:  TRUNC(-3.2)  
OUTPUT: -3  


INPUT:  TRUNC(3.2)  
OUTPUT:  3  


Parameter Summary
                                                                                                                                       * Name: TRUNC

                                                                                                                                       * Number of parameters: 1

                                                                                                                                       * Parameter types: number

________________


30. CEIL
Signature
CEIL(x)


Function Type
 Math Functions
Description
 Returns the smallest integer greater than or equal to X.
Examples
INPUT:  CEIL(-3.2)  
OUTPUT: -3  


INPUT:  CEIL(3.2)  
OUTPUT:  4  


Parameter Summary
                                                                                                                                          * Name: CEIL

                                                                                                                                          * Number of parameters: 1

                                                                                                                                          * Parameter types: number

________________


31. FLOOR
Signature
FLOOR(x)


Function Type
 Math Functions
Description
 Returns the largest integer less than or equal to X.
Examples
INPUT:  FLOOR(-3.2)  
OUTPUT: -4  


INPUT:  FLOOR(3.2)  
OUTPUT:  3  


Parameter Summary
                                                                                                                                             * Name: FLOOR

                                                                                                                                             * Number of parameters: 1

                                                                                                                                             * Parameter types: number

________________


32. RND
Signature
RND()


Function Type
 Math Functions
Description
 Generates a pseudorandom double‑precision value between 0 (inclusive) and 1 (exclusive).
Example
INPUT:  RND()  
OUTPUT: 0.3{...}  


Parameter Summary
                                                                                                                                                * Name: RND

                                                                                                                                                * Number of parameters: 0

                                                                                                                                                * Parameter types: none

________________






33. VAL
Signature
VAL(s)


Function Type
 Math Functions
Description
 Converts the string argument to its floating‑point numeric value. Ignores any non‑numeric suffix.
Example
INPUT:  VAL("3.1")  
OUTPUT: 3.1  


Parameter Summary
                                                                                                                                                   * Name: VAL

                                                                                                                                                   * Number of parameters: 1

                                                                                                                                                   * Parameter types: string

________________


34. POW
Signature
POW(base, exponent)


Function Type
 Math Functions
Description
 Raises base to the power of exponent. For fractional or very large exponents, base must be greater than 0.
Example
INPUT:  POW(451, 2)  
OUTPUT: 203401  


Parameter Summary
                                                                                                                                                      * Name: POW

                                                                                                                                                      * Number of parameters: 2

                                                                                                                                                      * Parameter types: number, number

________________


35. MIN
Signature
MIN(a, b)


Function Type
 Math Functions
Description
 Returns the smaller of the two arguments.
Example
INPUT:  MIN(2, 3)  
OUTPUT: 2  


Parameter Summary
                                                                                                                                                         * Name: MIN

                                                                                                                                                         * Number of parameters: 2

                                                                                                                                                         * Parameter types: number, number

________________


36. MAX
Signature
MAX(a, b)


Function Type
 Math Functions
Description
 Returns the larger of the two arguments.
Example
INPUT:  MAX(2, 3)  
OUTPUT: 3  


Parameter Summary
                                                                                                                                                            * Name: MAX

                                                                                                                                                            * Number of parameters: 2

                                                                                                                                                            * Parameter types: number, number

________________


37. MOD
Signature
MOD(m, n)


Function Type
 Math Functions
Description
 Returns the remainder of dividing m by n.
Example
INPUT:  MOD(451, 2)  
OUTPUT: 1  


Parameter Summary
                                                                                                                                                               * Name: MOD

                                                                                                                                                               * Number of parameters: 2

                                                                                                                                                               * Parameter types: number, number

________________


38. NUM
Signature
NUM(expr)


Function Type
 Math Functions
Description
 Attempts to convert the given expression (e.g. a string with currency symbols) to a numeric value.
Example
INPUT:  NUM("$100.00")  
OUTPUT: 100.00  


Parameter Summary
                                                                                                                                                                  * Name: NUM

                                                                                                                                                                  * Number of parameters: 1

                                                                                                                                                                  * Parameter types: string

________________


39. SUM
Signature
SUM(x1, x2, …, xN)


Function Type
 Math Functions
Description
 Returns the sum of all provided arguments. Supports any number of parameters.
Example
INPUT:  SUM(1, 2, 3, 4)  
OUTPUT: 10  


Parameter Summary
                                                                                                                                                                     * Name: SUM

                                                                                                                                                                     * Number of parameters: N (one or more)

                                                                                                                                                                     * Parameter types: number, …

________________


40. DATE_FORMAT
Signature
DATE_FORMAT(date_input, format)


Function Type
 Date Functions
Description
 Reformats date_input according to the given PHP‑style format string.
Example
INPUT:  DATE_FORMAT(DATE_DEFAULT("m/d/Y"), "m/d/Y")  
OUTPUT: (today’s date in “MM/DD/YYYY” form)  


Common Use Case
                                                                                                                                                                        * Dynamically insert today’s date into a field.

                                                                                                                                                                           * Element slug: user-milestones…, user-sources-source-code-date

________________


41. DATE_ADD
Signature
DATE_ADD(datePart, interval, date)


Function Type
 Date Functions
Description
 Adds the specified interval of datePart (second/minute/hour/day/month/year) to date.
Example
INPUT:  DATE_ADD(
           "hour", 
           4, 
           DATE_READ( DATE_DEFAULT("m/d/Y"), "m/d/Y" )
         )
OUTPUT: (UTC now + 4 hours, formatted as “MM/DD/YYYY”)  


Common Use Case
                                                                                                                                                                              * Dynamically add today’s date and adjust for a timezone offset (e.g. UTC → ET).

                                                                                                                                                                                 * Element slug: user-milestones…, user-sources-source-code-date

________________


42. DB_MAP
Signature
DB_MAP(type, input, match, output, default)


Function Type
 Maps and Lists
Description
 Maps an external term or code to an internal “Element” value by querying the specified database type.
Examples
INPUT:  
  DB_MAP("term",   "column", "name", "guid", "if untranslatable")  
  → maps an external “term” value in `column` to its Element GUID.  


INPUT:  
  DB_MAP("major",  "column", "name", "guid", "if untranslatable")  
  → maps an external “major” to its Element GUID.  


Common Entity Types
                                                                                                                                                                                    * Application Profile:

                                                                                                                                                                                       * user-applications-term / user-education-term

                                                                                                                                                                                       * user-applications-major / user-education-preferred-major

________________


43. Default Literal
Signature
"default_text"


Function Type
 Default
Description
 Sets a field’s value to the given literal string.
Examples
INPUT:  "taxonomyID"  
OUTPUT: (field is set to literal “taxonomyID”)  


INPUT:  "Submitted"  
OUTPUT: (status field is set to “Submitted”)  


Common Entity Types
                                                                                                                                                                                          * Profile: user-labels-import

                                                                                                                                                                                          * Application: user-applications-status

________________


44. DS_MAP
Signature
DS_MAP(input, data_source, match, output, default)


Function Type
 Maps and Lists
Description
 Like DB_MAP, but looks up values in a data‐source table (client.data_source), matching on the raw input.
Example
INPUT:  
  DS_MAP(
    "column", 
    "client.data_source", 
    "name", 
    "guid", 
    "if untranslatable"
  )  
OUTPUT: (the GUID in that data_source where name=column)  


Common Entity Types
                                                                                                                                                                                             * user-applications-major

                                                                                                                                                                                             * user-education-preferred-major

________________


45. DS_MAP (Nested)
Signature
DS_MAP(
  DS_MAP([...multiple data_source lookups...]),
  "data_source.majors",
  "code",
  "guid",
  default
)


Function Type
 Maps and Lists
Description
 Chains a series of DS_MAP calls (to normalize multiple source columns) and then a DB_MAP or final DS_MAP to resolve to the ultimate GUID.
Example
INPUT:  
  DS_MAP(
    DS_MAP([C28],"school.data_source.61599","column_2","column_1"),
    …,
    DB_MAP("major",[C28],"cip","code","mnm")
  )  
OUTPUT: (final major GUID)  


________________


46. IF
Signature
IF(condition, value_if_true, value_if_false)


Function Type
 Logic / Conditional
Description
 Evaluates a single (or nested) condition; returns one of two values.
Examples
INPUT:  IF(column="Hispanic/Latino","TRUE","")  
INPUT:  IF(column="Y","TRUE","")  
INPUT:  IF(
           condition1, 
           result1,
           IF(condition2, result2, "")
         )  ← nested  


Common Entity Type
                                                                                                                                                                                                * Profile (e.g. Hispanic/Latino flag)

________________


47. IF + DATE_DIFF + DATE_FORMAT
Signature
IF(
  DATE_DIFF("year",
            DATE_DEFAULT("Y"),
            DATE_FORMAT(RIGHT([C12],4),"Y")
  ) > 25,
  "value 1",
  "value 2"
)


Function Type
 Logic + Date
Description
 Computes age from a DOB column and assigns one of two values based on an age threshold.
Use Case
                                                                                                                                                                                                   * Add a value based on date‑of‑birth being over 25 years.

________________


48. SPLIT_INDEX
Signature
SPLIT_INDEX(text, delimiter, index)


Function Type
 Text Functions
Description
 Splits text on delimiter and returns the Nth segment.
Examples
INPUT:  SPLIT_INDEX("Justin Duong"," ",1)  → "Justin"  
INPUT:  SPLIT_INDEX("Justin Duong"," ",2)  → "Duong"  


Common Entity Type
                                                                                                                                                                                                      * Profile Guardian Names:

                                                                                                                                                                                                         * user-family-guardian-1-first-name

                                                                                                                                                                                                         * user-family-guardian-2-first-name

________________


49. ZIPCODE SUBSTR+IF+STRLEN+PAD
Signature
SUBSTR(
  IF(STRLEN([C13])=4,
     PAD([C13],0,5),
  IF(STRLEN([C13])=8,
     PAD([C13],0,9),
     [C13]
  )),
  0,
  5
)


Function Type
 Text + Logic
Description
 Pads 4‑ or 9‑digit ZIP codes, then takes only the first 5 characters.
Use Case
                                                                                                                                                                                                            * Import only the 5‑digit portion when both 5‑ and 9‑digit codes are present, padding leading zeros.

________________


50. TAXONOMY_MAP
Signature
TAXONOMY_MAP(source, match, output, default)


Function Type
 Maps and Lists
Description
 Fetches taxonomy terms (value ↔ GUID ↔ name) for a custom source or status field.
Examples
INPUT:  TAXONOMY_MAP(CODE,"value","guid","")  
INPUT:  TAXONOMY_MAP([user-applications-board-status],
                    "guid","name","value if not found")


Entity Type
                                                                                                                                                                                                               * Application board status (user-applications-board-status)

________________




51. REGEX_REPLACE
Formula/Example
INPUT: REGEXP_REPLACE("Hello World", "[a-z]", "x")
OUTPUT: "Hxxxx Wxxxx"


Usage Example
Name of the function: REGEXP_REPLACE
Number of parameters: 3
Type of parameters: string, pattern, replaceWith


INPUT: REGEXP_REPLACE("Hello World", "[a-z]", "x")
OUTPUT: "Hxxxx Wxxxx"


________________


52. CHECKBOX_FIRST
Formula/Example
INPUT: CHECKBOX_FIRST("[{'checked':true,'text':'Asian'},{'checked':false,'text':'European'},{'checked':true,'text':'American'}]")
OUTPUT: "Asian"

Usage Example
Name of the function: CHECKBOX_FIRST
Number of parameters: 1
Type of parameters: json_input


INPUT: CHECKBOX_FIRST("[{'checked':true,'text':'Asian'},{'checked':false,'text':'European'},{'checked':true,'text':'American'}]")
OUTPUT: "Asian"


INPUT: CHECKBOX_FIRST("[{'checked':false,'text':'Asian'},{'checked':false,'text':'European'},{'checked':false,'text':'American'}]")
OUTPUT: "”



________________

53. CONTAINS
Formula/Example
INPUT: CONTAINS("Hello World", "Hello")
OUTPUT: TRUE


INPUT: CONTAINS("Hello World", "random string")
OUTPUT: FALSE




Usage Example
Name of the function: CONTAINS
Number of parameters: 2
Type of parameters: string, substr


INPUT: CONTAINS("Hello World", "Hello")
OUTPUT: TRUE


INPUT: CONTAINS("Hello World", "random string")
OUTPUT: FALSE


________________
54. HAS_ONE_TRUE
Formula/Example
INPUT: HAS_ONE_TRUE("[{'associated_degree':false},{'associated_degree':true,'text':'European'}]", "associated_degree")
OUTPUT: TRUE

Usage Example
Name of the function: HAS_ONE_TRUE
Number of parameters: 2
Type of parameters: json_input, attribute


INPUT: HAS_ONE_TRUE("[{'associated_degree':false},{'associated_degree':true,'text':'European'}]", "associated_degree")
OUTPUT: TRUE


________________


55. STARTS_WITH
Formula/Example
INPUT: STARTS_WITH("Hello World", "Hello")
OUTPUT: TRUE 


Usage Example
Name of the function: STARTS_WITH
Number of parameters: 2
Type of parameters: string, substr


INPUT: STARTS_WITH("Hello World", "Hello")
OUTPUT: TRUE


________________


56. ENDS_WITH
Formula/Example
INPUT: ENDS_WITH("Hello World", "World")
OUTPUT: TRUE


Usage Example
Name of the function: ENDS_WITH
Number of parameters: 2
Type of parameters: string, substr


INPUT: ENDS_WITH("Hello World", "World")
OUTPUT: TRUE
