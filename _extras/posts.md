```meta-bind-button
label: New Post
hidden: false
class: ""
tooltip: ""
id: ""
style: primary
actions:
  - type: templaterCreateNote
    templateFile: _extras/templates/post.md
    folderPath: _extras
    fileName: Untitled
    openNote: true
```

---
### Templates
- [[post]]

# Posts
```dataview
table date, title
where !contains(file.path,"_extras")
sort file.name desc
limit 15
```