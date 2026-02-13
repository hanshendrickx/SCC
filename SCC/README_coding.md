




# ⚠️ Minor differences to be aware of
Feature	cmd	PowerShell
Virtual env activation	.venv\Scripts\activate	same
Set environment var	set VAR=value	$env:VAR="value"
List files	dir	ls or dir
Copy/paste	Right-click or Ctrl+C/Ctrl+V (enable in properties)	Ctrl+Shift+C/V
Command history	doskey /history	Get-History or up/down arrows
But for 99% of Django work, the commands are identical. The framework doesn’t care which shell you use.