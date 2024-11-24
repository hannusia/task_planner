drop keyspace if exists feedback_data;
create keyspace feedback_data with replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '2'};


use feedback_data;
create table feedbacks ( id UUID PRIMARY KEY, username text, feedback_text text );


insert into feedback_data.feedbacks ( id, username, feedback_text )
VALUES( uuid(), 'John', 'Pretty Good' );

insert into feedback_data.feedbacks ( id, username, feedback_text )
VALUES( uuid(), 'Nathan', 'Ohh, very nice' );

insert into feedback_data.feedbacks ( id, username, feedback_text )
VALUES( uuid(), 'Steve', 'I like it!' );
