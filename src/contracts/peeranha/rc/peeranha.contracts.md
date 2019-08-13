<h1 class="contract">registeracc</h1>
### Parameters
Input parameters:

* `user`
* `display_name`
* `ipfs_profile`
* `ipfs_avatar`

Implied parameters: 

* `account_name`
* `string`
* `string`
* `string`

<h1 class="contract">setaccstrprp</h1>
### Parameters
Input parameters:

* `user`
* `key`
* `value`

Implied parameters: 

* `account_name`
* `uint8`
* `string`

<h1 class="contract">setaccintprp</h1>
### Parameters
Input parameters:

* `user`
* `key`
* `value`

Implied parameters: 

* `account_name`
* `uint8`
* `string`

<h1 class="contract">setaccprof</h1>
### Parameters
Input parameters:

* `user`
* `ipfs_profile`
* `display_name`

Implied parameters: 

* `account_name`
* `string`
* `string`

<h1 class="contract">postquestion</h1>
### Parameters
Input parameters:

* `user`
* `community_id`
* `tags`
* `title`
* `ipfs_link`

Implied parameters: 

* `account_name`
* `uint16`
* `uint32[]`
* `string`
* `string`

<h1 class="contract">postanswer</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `ipfs_link`

Implied parameters: 

* `account_name`
* `uint64`
* `string`

<h1 class="contract">postcomment</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`
* `ipfs_link`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`
* `string`

<h1 class="contract">delquestion</h1>
### Parameters
Input parameters:

* `user`
* `question_id`

Implied parameters: 

* `account_name`
* `uint64`

<h1 class="contract">delanswer</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`

<h1 class="contract">delcomment</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`
* `comment_id`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`
* `uint16`


<h1 class="contract">modquestion</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `community_id`
* `tags`
* `title`
* `ipfs_link`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`
* `uint32[]`
* `string`
* `string`

<h1 class="contract">modanswer</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`
* `ipfs_link`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`
* `string`

<h1 class="contract">modcomment</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`
* `comment_id`
* `ipfs_link`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`
* `uint16`
* `string`

<h1 class="contract">upvote</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`

<h1 class="contract">downvote</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`

<h1 class="contract">votedelete</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`
* `comment_id`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`
* `uint16`

<h1 class="contract">mrkascorrect</h1>
### Parameters
Input parameters:

* `user`
* `question_id`
* `answer_id`

Implied parameters: 

* `account_name`
* `uint64`
* `uint16`

<h1 class="contract">crcommunity</h1>
### Parameters
Input parameters:

* `user`
* `name`
* `ipfs_description`

Implied parameters: 

* `account_name`
* `string`
* `string`

<h1 class="contract">crtag</h1>
### Parameters
Input parameters:

* `user`
* `name`
* `ipfs_description`

Implied parameters: 

* `account_name`
* `string`
* `string`

<h1 class="contract">vtcrcomm</h1>
### Parameters
Input parameters:

* `user`
* `community_id`

Implied parameters: 

* `account_name`
* `uint32`

<h1 class="contract">vtcrtag</h1>
### Parameters
Input parameters:

* `user`
* `community_id`
* `tag_id`

Implied parameters: 

* `account_name`
* `uint16`
* `uint32`

<h1 class="contract">vtdelcomm</h1>
### Parameters
Input parameters:

* `user`
* `community_id`

Implied parameters: 

* `account_name`
* `uint32`

<h1 class="contract">vtdeltag</h1>
### Parameters
Input parameters:

* `user`
* `community_id`
* `tag_id`

Implied parameters: 

* `account_name`
* `uint16`
* `uint32`

