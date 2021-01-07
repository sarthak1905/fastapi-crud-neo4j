from neomodel import StructuredRel, StructuredNode, RelationshipTo, RelationshipFrom
from neomodel import (StringProperty, BooleanProperty, FloatProperty, IntegerProperty, 
    ArrayProperty, JSONProperty, DateTimeProperty, UniqueIdProperty)

import uuid

#Relations
class Friendship(StructuredRel):
    since = DateTimeProperty(default_now=True)

class Post_Activity(StructuredRel):
    timestamp = DateTimeProperty(default_now=True)

class Membership(StructuredRel):
    since = DateTimeProperty(default_now=True)

#Models
class User(StructuredNode):
    #Attributes
    first_name     = StringProperty(required=True)
    last_name      = StringProperty(required=True)
    ph_number      = StringProperty(required=True)  
    username       = StringProperty(unique_index=True, required=True)

    #Relationships
    friend         = RelationshipTo('User', 'FRIENDS_WITH', model=Friendship)
    written        = RelationshipTo('Post', 'HAS', model=Post_Activity)
    liked          = RelationshipTo('Post', 'LIKED', model=Post_Activity)
    shared         = RelationshipTo('Post', 'SHARED', model=Post_Activity)
    commented      = RelationshipTo('Post', 'COMMENTED', model=Post_Activity)
    residence      = RelationshipTo('Location', 'BELONGS_TO')
    membership     = RelationshipTo('GroupChat', 'IS_MEMBER', model=Membership)

    def to_json(self):
        props = self.__properties__
        props['id'] = props['node_id']
        del props['node_id']
        return props


class Post(StructuredNode):
    #Attributes
    post_id                  = StringProperty(unique_index=True, required=True)
    has_media                = BooleanProperty(default=False)
    content                  = StringProperty(defalut=[])
    likes                    = ArrayProperty(default=0)
    comments                 = ArrayProperty(default=[])
    shares                   = ArrayProperty(default=0)

    #Relationships
    author                   = RelationshipFrom('User', 'HAS', model=Post_Activity) 
    liked_by                 = RelationshipFrom('User', 'LIKED', model=Post_Activity)
    shared_by                = RelationshipFrom('User', 'SHARED', model=Post_Activity)
    commented_by             = RelationshipFrom('User', 'COMMENTED', model=Post_Activity)
    popularity               = RelationshipTo('Trending', 'IS')

class Location(StructuredNode):
    #Attributes
    city                     = StringProperty(default="")
    country                  = StringProperty(default="")
    zip_code                 = IntegerProperty(required=True, unique_index=True)

    #Relationships
    resident                 = RelationshipFrom('User','BELONGS_TO')

class GroupChat(StructuredNode):
    #Attributes
    group_id                 = StringProperty(unique_index=True, required=True)
    members                  = ArrayProperty(default=[])

    #Relationships
    membership               = RelationshipFrom('User', 'IS_IN', model=Membership)

class Trending(StructuredNode):
    #Attributes
    trend_id                 = StringProperty(unique_index=True, required=True)
    likes                    = IntegerProperty(default=0)
    comments                 = IntegerProperty(default=0)
    sharers                  = IntegerProperty(default=0)

    #Relationships 
    popular                  = RelationshipFrom('Post', 'IS')