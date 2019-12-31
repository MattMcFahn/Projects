CREATE TABLE dated_headlines_log(
dated_article_key VARCHAR(200) PRIMARY KEY,
article_key VARCHAR(180) NOT NULL,
datetime TIMESTAMP NOT NULL,
newssource VARCHAR(30) NOT NULL,
article_type VARCHAR(80) NOT NULL,
headline VARCHAR(80) NOT NULL,
weblink VARCHAR(150) NOT NULL
);

CREATE TABLE headlines_master(
article_key VARCHAR(180) PRIMARY KEY,
datetime TIMESTAMP NOT NULL,
newssource VARCHAR(30) NOT NULL,
article_type VARCHAR(80) NOT NULL,
headline VARCHAR(80) NOT NULL,
weblink VARCHAR(150) NOT NULL
);

