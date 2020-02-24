SELECT
	posts.id as id,
	posts.title as title,
	usr.username as username,
	posts.created_at as pbdate,
	group_concat(distinct ct.catag_name)
FROM
	posts AS posts
LEFT JOIN zipper_posts_catstags AS zp ON
	posts.id = zp.post_id
LEFT JOIN users AS usr ON posts.user_id = usr.id
LEFT JOIN catstags AS ct ON zp.catag_id = ct.id
GROUP BY 1, 2, 3, 4;