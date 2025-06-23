Additional future markup extension for enzo maybe:
---
import("Avatar", "./Avatar.enzo");
import("ActionList", "./ActionList.enzo");

export($user);
$user: {
  $name:       "Alice Bridges",
  $avatarUrl:  "/images/alice.png",
  $bio:        "UX designer and cat lover.",
  $hobbies:    ["Cycling", "Photography", "Gardening"]
};

export($showHobbies);
$showHobbies: false;

hobbiesMd: (
  return(
    join(
      map(
        ( $h; "- < $h >" ),
        $user.hobbies
      ),
    "\n")
  );
)
---

# Welcome, < $user.name >

Here is your avatar:

<Avatar: {
   name:    " <$user.name> ",
   src:     "<$user.avatarUrl> ",
   size:    128
}>

> **About Me**
> <$user.bio>

## Hobbies

Below is my personal list of hobbies as Markdown bullets:

<hobbiesMd();>

## Actions

Toggle display of my hobbies:

<ActionList: {
   itemsMd:   "<hobbiesMd();>",
   isOpen<:   $showHobbies
}>

Some final static Markdown text can continue here.

+++
.avatar {
  border-radius: 50%;
  border: 2px solid #ccc;
}
.bio-blockquote {
  font-style: italic;
  color: #555;
  margin: 1rem 0;
}
.action-list {
  margin-top: 1rem;
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
}
+++
