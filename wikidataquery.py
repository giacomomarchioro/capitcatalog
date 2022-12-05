import requests

url = 'https://query.wikidata.org/sparql'
query = '''
SELECT DISTINCT ?item ?label
WHERE
{
  SERVICE wikibase:mwapi
  {
    bd:serviceParam wikibase:endpoint "www.wikidata.org";
                    wikibase:api "Generator";
                    mwapi:generator "search";
                    mwapi:gsrsearch "inlabel:city"@en;
                    mwapi:gsrlimit "max".
    ?item wikibase:apiOutputItem mwapi:title.
  }
  ?item rdfs:label ?label. FILTER( LANG(?label)="en" )

  # … at this point, you have matching ?item(s) 
  # and can further restrict or use them
  # as in any other SPARQL query

  # Example: the following restricts the matches
  # to college towns (Q1187811) only

  ?item wdt:P31 wd:Q1187811 .
}
'''

query = '''
SELECT DISTINCT ?item ?label
WHERE
{
  SERVICE wikibase:mwapi
  {
    bd:serviceParam wikibase:endpoint "www.wikidata.org";
                    wikibase:api "Generator";
                    mwapi:generator "search";
                    mwapi:gsrsearch "inlabel:city"@en;
                    mwapi:gsrlimit "max".
    ?item wikibase:apiOutputItem mwapi:title.
  }
  ?item rdfs:label ?label. FILTER( LANG(?label)="en" )

  # … at this point, you have matching ?item(s) 
  # and can further restrict or use them
  # as in any other SPARQL query

  # Example: the following restricts the matches
  # to college towns (Q1187811) only

  ?item wdt:P31 wd:Q1187811 .
}
'''


query = ''' SELECT ?item ?itemLabel ?linkcount WHERE { ?item wdt:P31/wdt:P279* wd:Q35666 . ?item wikibase:sitelinks ?linkcount . FILTER (?linkcount >= 1) . SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" . } } GROUP BY ?item ?itemLabel ?linkcount ORDER BY DESC(?linkcount) ''' 
r = requests.get(url, params = {'format': 'json', 'query': query}) 
data = r.json()

g = requests.get(r'https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Isotta&format=json&errorformat=plaintext&language=it&uselang=it&type=item',params = {'format': 'json'})
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()


fetch("https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Isotta&format=json&errorformat=plaintext&language=it&uselang=it&type=item", {
  method: 'post',
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  },
}).then(function(res){
  return res.json(); //error here
}).then(function(data){
  console.log(data);
}).catch((error) => {
  console.log(error);
});


let url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Isotta&format=json&errorformat=plaintext&language=it&uselang=it&type=item&origin=*";

fetch(url).then(res => res.json()).then(out =>console.log('Checkout this JSON! ', out)).catch(err => throw err);


getJSON("https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Isotta&format=json&errorformat=plaintext&language=it&uselang=it&type=item&origin=*",
function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
    alert('Your query count: ' + data.query.count);
  }
});



var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

If you want to do it in plain javascript, you can define a function like this:

var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

mydata = getJSON("https://www.wikidata.org/w/api.php?action=wbsearchentities&search=Isotta&format=json&errorformat=plaintext&language=it&uselang=it&type=item&origin=*",
function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
    alert('Your query count: ' + data.query.count);
  }
});

https://www.wikidata.org/w/api.php?action=wbsearchentities&ids=Q16550450&format=json&errorformat=plaintext&language=it&uselang=it&type=item&origin=*

https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q16550450&format=json&languages=it