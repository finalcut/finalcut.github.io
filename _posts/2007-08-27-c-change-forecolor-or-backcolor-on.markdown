---
layout: post
title: "C#: Change ForeColor or BackColor on the actual tab of a TabControl"
date: 2007-08-27
comments: false
category: [c#,.net]
tags: [ui,tabcontrol]
---
Exciting? Not exactly - but it is useful. Amazingly enough you can't just set
a property on the tab to change the tab's fore or back color - the forecolor
and backcolor properties control the contents of the tab but not the tab label
itself. Here is how you do it:



First you need to set your tab controls draw mode to
TabDrawMode.OwnerDrawFixed - this lets you override the normal drawing method
with your own. Then you need to add an event handler to your tab controls
DrawItem event


```c#
this.tabParamType.DrawMode = TabDrawMode.OwnerDrawFixed;
this.tabParamType.DrawItem += new DrawItemEventHandler(tabParamType_DrawItem);


void tabParamType_DrawItem(object sender, DrawItemEventArgs e)
{
  Color foreColor = System.Drawing.SystemColors.ControlText;
  string tabName = this.tabParamType.TabPages[e.Index].Text;

  /* some logic to determine the color of the text - basically if the name
  contains an asterix make the text red, then make a weak effort to remove the
  asterix from what we actually show
  */
  if (tabName.IndexOf("*") > 0)
  {
    foreColor = Color.Red;
    tabName = tabName.TrimEnd('*');
  }

  UIHelper.DrawTabText(this.tabParamType, e, foreColor, tabName);

}


```



Inside that event handler call one of these three methods:


```c#
public static void DrawTabText(TabControl tabControl, DrawItemEventArgse, string caption)
{
  Color backColor = (Color)System.Drawing.SystemColors.Control;
  Color foreColor = (Color)System.Drawing.SystemColors.ControlText;
  DrawTabText(tabControl, e, backColor, foreColor, caption);
}
public static void DrawTabText(TabControl tabControl, DrawItemEventArgs e, System.Drawing.Color foreColor, string caption)
{
  Color backColor = (Color)System.Drawing.SystemColors.Control;
  DrawTabText(tabControl, e, backColor, foreColor, caption);
}

public static void DrawTabText(TabControl tabControl, DrawItemEventArgs e, System.Drawing.Color backColor, System.Drawing.Color foreColor, string caption)
{
  #region setup
  Font tabFont;
  Brush foreBrush = new SolidBrush(foreColor);
  Rectangle r = e.Bounds;
  Brush backBrush = new SolidBrush(backColor);
  string tabName = tabControl.TabPages[e.Index].Text;
  StringFormat sf = new StringFormat();
  sf.Alignment = StringAlignment.Center;
  #endregion

  #region drawing
  e.Graphics.FillRectangle(backBrush, r);

  r = new Rectangle(r.X, r.Y + 3, r.Width, r.Height - 3);
  if (e.Index == tabControl.SelectedIndex)
  {
    tabFont = new Font(e.Font, FontStyle.Italic);
    tabFont = new Font(tabFont, FontStyle.Bold);
  }
  else
  {
    tabFont = e.Font;
  }

  e.Graphics.DrawString(caption, tabFont, foreBrush, r, sf);
  #endregion

  #region cleanup
  sf.Dispose();
  if (e.Index == tabControl.SelectedIndex)
  {
    tabFont.Dispose();
    backBrush.Dispose();
  }
  else
  {
    backBrush.Dispose();
    foreBrush.Dispose();
  }
  #endregion

}

```


Now, I created three versions so that I can optionally pass in the fore or
back color - just in case i get in the habit of overriding my tab controls
draw mode.



This technique was based entirely off of a post by ["Rajesh" on his
blog](http://rajeshkm.blogspot.com/2006/07/how-to-change-color-of-tab-control-
in.html)

## Comments

r3m0t

Here's a version which is much closer to the behaviour of TabDrawMode.Normal,
in terms of the text positioning. In fact, on my machine it is pixel-for-pixel
identical. In my case, HotTrack is False, SizeMode is Normal, Multiline is
False, and I'm using Windows XP with the Classic theme.

http://pastebin.com/f39b309bd

Bill

I really don't know. I still haven't experienced this problem and I've used
the tab painting technique in a couple projects.

Sorry I can't be any more help

Guillaume

i have the same problem as luke... and not finding any usefull help... any
clue ?

Bill

sorry I've been out of town the past 6 days.

I don't really know - I haven't experienced this problem at all. Perhaps
change the size of the rectangle you are painting in.

Luke

I get a transparent or grey color behind the tabs, is there anyway to change
this?
