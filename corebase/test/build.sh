#!/bin/sh

XMLFILE=$(base64 demoformat/demo.xml)
HASHXML=$(sha512sum demoformat/demo.xml | awk '{ print $1 }')
echo -e 'XMLFILE="""'$XMLFILE'"""\nHASHXML="""'$HASHXML'"""' > documents.py


ODFFILE=$(base64 demoformat/demo.odt)
HASHODF=$(sha512sum demoformat/demo.odt | awk '{ print $1 }')
echo -e 'ODFFILE="""'$ODFFILE'"""\nHASHODF="""'$HASHODF'"""' >> documents.py

DOCXFILE=$(base64 demoformat/demo.docx)
HASHDOCX=$(sha512sum demoformat/demo.docx | awk '{ print $1 }')
echo -e 'DOCXFILE="""'$DOCXFILE'"""\nHASHDOCX="""'$HASHDOCX'"""' >> documents.py
