#!/usr/bin

pip install pylint
pip install django-extensions
pip install pygraphviz

BASEDOT=docs/_static/dot
BASEPNG=docs/_static/png

mkdir -p $BASEDOT
mkdir -p $BASEPNG

sed -i s/\#\'django_extensions\'/\'django_extensions\'/g dfva/settings.py
############# INSTITUTION ############################

# Institution Serializer 

pyreverse src/institution/serializer.py src/corebase/serializer.py src/institution/authenticator/serializer.py  src/institution/signer/serializer.py src/institution/validator/serializer.py  src/corebase/rsa.py  src/corebase/authenticate.py src/corebase/signer.py src/corebase/validator.py 
cat classes.dot | grep -v "{Meta|fields" > $BASEDOT/institution_serializer.dot
mv packages.dot $BASEDOT/packages_institution_serializer.dot

dot -Tpng $BASEDOT/institution_serializer.dot -o $BASEPNG/institution_serializer.png
dot -Tpng $BASEDOT/packages_institution_serializer.dot -o $BASEPNG/packages_institution_serializer.png

# Institution  Views 

pyreverse src/institution/views.py src/institution/authenticator/views.py src/institution/signer/views.py src/institution/validator/views.py src/corebase/views.py src/corebase/rsa.py
mv packages.dot $BASEDOT/packages_institution_views.dot
mv classes.dot $BASEDOT/institution_views.dot

dot -Tpng $BASEDOT/packages_institution_views.dot -o $BASEPNG/packages_institution_views.png
dot -Tpng $BASEDOT/institution_views.dot -o $BASEPNG/institution_views.png

# Institution Models

python src/manage.py graph_models corebase institution > $BASEDOT/institution_model.dot
dot -Tpng $BASEDOT/institution_model.dot -o $BASEPNG/institution_model.png


################ PERSON #######################################


# Person Serializer
pyreverse src/person/serializer.py  src/corebase/serializer.py  src/person/authenticator/serializer.py src/person/signer/serializer.py  src/person/validator/serializer.py src/corebase/authenticate.py src/corebase/signer.py src/corebase/validator.py 
cat classes.dot | grep -v "{Meta|fields" > $BASEDOT/person_serializer.dot
mv packages.dot $BASEDOT/packages_person_serializer.dot

dot -Tpng $BASEDOT/person_serializer.dot -o $BASEPNG/person_serializer.png
dot -Tpng $BASEDOT/packages_person_serializer.dot -o $BASEPNG/packages_person_serializer.png

# Person  Views 
pyreverse src/person/views.py src/corebase/views.py src/person/authenticator/views.py  src/person/signer/views.py src/person/validator/views.py src/corebase/rsa.py 
mv packages.dot $BASEDOT/packages_person_views.dot
mv classes.dot $BASEDOT/person_views.dot

dot -Tpng $BASEDOT/packages_person_views.dot -o $BASEPNG/packages_person_views.png
dot -Tpng $BASEDOT/person_views.dot -o $BASEPNG/person_views.png

# Person Models

python src/manage.py graph_models corebase person > $BASEDOT/person_model.dot
dot -Tpng $BASEDOT/person_model.dot -o $BASEPNG/person_model.png

# CA management

pyreverse src/corebase/ca_management/
mv packages.dot $BASEDOT/ca_management_packages.dot
mv classes.dot $BASEDOT/ca_management_clases.dot

dot -Tpng $BASEDOT/ca_management_packages.dot -o $BASEPNG/ca_management_packages.png
dot -Tpng $BASEDOT/ca_management_clases.dot -o $BASEPNG/ca_management_clases.png

sed -i s/\'django_extensions\'/\#\'django_extensions\'/g dfva/settings.py
