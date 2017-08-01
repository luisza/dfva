#!/bin/sh

XMLFILE=$(base64 demoformat/demo.xml)
HASHXML=$(sha512sum demoformat/demo.xml | awk '{ print $1 }')
echo -e 'XMLFILE="""'$XMLFILE'"""\nHASHXML="""'$HASHXML'"""' > xmlfile.py


ODFFILE=$(base64 demoformat/demo.odt)
HASHODF=$(sha512sum demoformat/demo.odt | awk '{ print $1 }')
echo -e 'ODFFILE="""'$ODFFILE'"""\nHASHODF="""'$HASHODF'"""' > odffile.py

DOCXFILE=$(base64 demoformat/demo.docx)
HASHDOCX=$(sha512sum demoformat/demo.docx | awk '{ print $1 }')
echo -e 'DOCXFILE="""'$DOCXFILE'"""\nHASHDOCX="""'$HASHDOCX'"""' > docxfile.py
