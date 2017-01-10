db();
db //sqlite connection
c //cursor
idc //int loaded idcount number
tagListCache //0 or cached taglist
allListCache //0 or cached allList

/*--- modifier functions ---*/
loadIdCount(); //laods idcount file or creates id count
//add entry to db without commiting. tags must be comma sepearated
//string of tags
add(title,ttype,cover,link,tags,int wide);
commit(); //commit db
//add tags to entry with id idc. tags must be array of strings
addTags(int idc,tags);
//update field of entry with id eid
updateEntry(int eid,string field,string value);
//add given tags in tag array to entry with specified eid
updateTags(int eid,tags);
//remove entry with specified eid
remove(int eid);

/*--- data access ---*/
getAll(); //return array of all entries from db
printTagList(); //print distinct tags
//get all entries with AND of input tags, tags must be string array
getTags(tags);

/*--- unused/debug ---*/
printTableAll(); //debug, print all
printAllTags(); //debug, print tags
getType(string type); //get all of a certain type
//execute given statement
dexecute(string command);
