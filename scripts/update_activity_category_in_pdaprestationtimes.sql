update extraschool_pdaprestationtimes set activitycategoryid = (select min(id) from extraschool_activitycategory);
