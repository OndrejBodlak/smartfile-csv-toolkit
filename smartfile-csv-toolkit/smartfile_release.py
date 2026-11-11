#!/usr/bin/env python3
"""SmartFile 1.0 - CSV Toolkit desktop release."""
from __future__ import annotations

import tkinter as tk
import sys
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

from smartfile import read_csv, remove_duplicates, write_csv


def resource_path(filename: str) -> Path:
    """Resolve bundled resources both in development and PyInstaller builds."""
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return bundle_dir / filename


class DnDCTk(ctk.CTk, TkinterDnD.DnDWrapper):
    """CustomTkinter root with tkinterdnd2 support."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


class SmartFileApp:
    BG = "#0B1020"
    PANEL = "#121A2B"
    PANEL_2 = "#182338"
    BORDER = "#26344D"
    TEXT = "#F3F6FC"
    MUTED = "#91A0B8"
    ACCENT = "#7567F8"
    GREEN = "#2CCB91"

    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.root.title("SmartFile 1.0 | CSV Toolkit")
        self.root.geometry("1180x760")
        self.root.minsize(980, 650)
        self.root.configure(fg_color=self.BG)
        try:
            self.root.iconbitmap(str(resource_path("smartfile.ico")))
        except tk.TclError:
            # The app remains usable if Windows cannot load the optional window icon.
            pass

        self.selected_files: list[Path] = []
        self.output_headers: list[str] = []
        self.output_rows: list[dict[str, str]] = []
        self.last_removed = 0

        self._style_tree()
        self._build_ui()
        self._enable_drag_and_drop()
        self._refresh_files()
        self._set_status("Ready to work. Import CSV files to get started.")

    def _style_tree(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Smart.Treeview", background="#101827", foreground=self.TEXT,
            fieldbackground="#101827", borderwidth=0, rowheight=34,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Smart.Treeview.Heading", background="#1C2940",
            foreground="#DCE5F5", relief="flat",
            font=("Segoe UI Semibold", 10)
        )
        style.map("Smart.Treeview", background=[("selected", "#403B83")],
                  foreground=[("selected", "#FFFFFF")])
        style.map("Smart.Treeview.Heading", background=[("active", "#263653")])

    def _card(self, parent, **kwargs):
        return ctk.CTkFrame(parent, fg_color=self.PANEL, corner_radius=14,
                            border_width=1, border_color=self.BORDER, **kwargs)

    def _button(self, parent, text, command, primary=False, width=None):
        return ctk.CTkButton(
            parent, text=text, command=command, width=width or 130, height=38,
            corner_radius=9, fg_color=self.ACCENT if primary else self.PANEL_2,
            hover_color="#5E52D6" if primary else "#263653",
            text_color="#FFFFFF", font=ctk.CTkFont("Segoe UI", 12, weight="bold")
        )

    def _build_ui(self) -> None:
        outer = ctk.CTkFrame(self.root, fg_color="transparent")
        outer.pack(fill="both", expand=True, padx=26, pady=22)

        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        brand = ctk.CTkFrame(header, fg_color="transparent")
        brand.pack(side="left")
        ctk.CTkLabel(brand, text="SmartFile", text_color=self.TEXT,
                     font=ctk.CTkFont("Segoe UI", 29, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(brand, text="CSV TOOLKIT  /  CLEAN • MERGE • INSPECT",
                     text_color=self.MUTED, font=ctk.CTkFont("Segoe UI", 10, weight="bold")).pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(header, text="LOCAL PROCESSING  •  YOUR FILES STAY ON YOUR DEVICE",
                     text_color=self.GREEN, font=ctk.CTkFont("Segoe UI", 10, weight="bold")).pack(side="right", pady=(15, 0))

        actions = self._card(outer)
        actions.pack(fill="x", pady=(0, 16))
        action_inner = ctk.CTkFrame(actions, fg_color="transparent")
        action_inner.pack(fill="x", padx=16, pady=14)
        self._button(action_inner, "+  Import CSV files", self._select_files, True, 165).pack(side="left", padx=(0, 9))
        self._button(action_inner, "Merge files", self._merge, width=125).pack(side="left", padx=5)
        self._button(action_inner, "Remove duplicates", self._dedupe, width=160).pack(side="left", padx=5)
        self._button(action_inner, "Export result  ↓", self._export, width=145).pack(side="right")

        stats = ctk.CTkFrame(outer, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 16))
        self.stat_values = {}
        for key, title, value, accent in [
            ("rows", "TOTAL ROWS", "0", self.ACCENT),
            ("columns", "COLUMNS", "0", "#3298D4"),
            ("duplicates", "DUPLICATES REMOVED", "0", self.GREEN),
        ]:
            card = self._card(stats)
            card.pack(side="left", fill="x", expand=True, padx=(0, 10))
            ctk.CTkFrame(card, fg_color=accent, width=4, corner_radius=3).pack(side="left", fill="y", padx=(0, 13), pady=12)
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(side="left", pady=10)
            ctk.CTkLabel(content, text=title, text_color=self.MUTED,
                         font=ctk.CTkFont("Segoe UI", 9, weight="bold")).pack(anchor="w")
            label = ctk.CTkLabel(content, text=value, text_color=self.TEXT,
                                 font=ctk.CTkFont("Segoe UI", 23, weight="bold"))
            label.pack(anchor="w", pady=(1, 0))
            self.stat_values[key] = label

        workspace = ctk.CTkFrame(outer, fg_color="transparent")
        workspace.pack(fill="both", expand=True)
        workspace.grid_columnconfigure(0, weight=1, minsize=280)
        workspace.grid_columnconfigure(1, weight=3)
        workspace.grid_rowconfigure(0, weight=1)

        files_card = self._card(workspace)
        files_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(files_card, text="SOURCE FILES", text_color=self.MUTED,
                     font=ctk.CTkFont("Segoe UI", 10, weight="bold")).pack(anchor="w", padx=16, pady=(16, 3))
        ctk.CTkLabel(files_card, text="Drop CSV files anywhere in this window", text_color="#7789A8",
                     font=ctk.CTkFont("Segoe UI", 9)).pack(anchor="w", padx=16, pady=(0, 7))
        self.file_list = ctk.CTkScrollableFrame(files_card, fg_color="transparent")
        self.file_list.pack(fill="both", expand=True, padx=9, pady=(0, 8))
        file_buttons = ctk.CTkFrame(files_card, fg_color="transparent")
        file_buttons.pack(fill="x", padx=12, pady=(0, 13))
        self._button(file_buttons, "Remove all", self._clear_files, width=110).pack(side="left")

        preview_card = self._card(workspace)
        preview_card.grid(row=0, column=1, sticky="nsew")
        preview_head = ctk.CTkFrame(preview_card, fg_color="transparent")
        preview_head.pack(fill="x", padx=16, pady=(15, 10))
        ctk.CTkLabel(preview_head, text="RESULT PREVIEW", text_color=self.MUTED,
                     font=ctk.CTkFont("Segoe UI", 10, weight="bold")).pack(side="left")
        self.preview_hint = ctk.CTkLabel(preview_head, text="No data loaded",
                     text_color=self.MUTED, font=ctk.CTkFont("Segoe UI", 10))
        self.preview_hint.pack(side="right")

        table_wrap = ctk.CTkFrame(preview_card, fg_color="#101827", corner_radius=9)
        table_wrap.pack(fill="both", expand=True, padx=13, pady=(0, 13))
        self.tree = ttk.Treeview(table_wrap, style="Smart.Treeview", show="headings")
        ybar = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview)
        xbar = ttk.Scrollbar(table_wrap, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=(8, 0))
        ybar.grid(row=0, column=1, sticky="ns", pady=(8, 0))
        xbar.grid(row=1, column=0, sticky="ew", padx=(8, 0), pady=(0, 8))
        table_wrap.grid_rowconfigure(0, weight=1)
        table_wrap.grid_columnconfigure(0, weight=1)

        footer = ctk.CTkFrame(outer, fg_color="transparent")
        footer.pack(fill="x", pady=(13, 0))
        self.status = ctk.CTkLabel(footer, text="", text_color=self.MUTED,
                                   font=ctk.CTkFont("Segoe UI", 10))
        self.status.pack(side="left")
        ctk.CTkLabel(footer, text="SMARTFILE 1.0  •  OFFLINE & PRIVATE",
                     text_color="#64748B", font=ctk.CTkFont("Segoe UI", 9, weight="bold")).pack(side="right")

    def _enable_drag_and_drop(self) -> None:
        """Accept files dropped anywhere on the application window."""
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self._on_drop)

    def _on_drop(self, event) -> None:
        try:
            dropped = self.root.tk.splitlist(event.data)
            added = 0
            skipped = 0
            for item in dropped:
                path = Path(item)
                if path.suffix.lower() != ".csv" or not path.is_file():
                    skipped += 1
                    continue
                if path not in self.selected_files:
                    self.selected_files.append(path)
                    added += 1
            self._refresh_files()
            message = f"Added {added} CSV file(s) by drag & drop."
            if skipped:
                message += f" Skipped {skipped} non-CSV or unavailable item(s)."
            self._set_status(message)
        except (OSError, tk.TclError) as exc:
            messagebox.showerror("Drop failed", f"Could not add the dropped files: {exc}")

    def _set_status(self, message: str) -> None:
        self.status.configure(text=message)

    def _refresh_files(self) -> None:
        for widget in self.file_list.winfo_children():
            widget.destroy()
        for index, path in enumerate(self.selected_files):
            row = ctk.CTkFrame(self.file_list, fg_color=self.PANEL_2, corner_radius=8)
            row.pack(fill="x", padx=2, pady=4)
            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, padx=9, pady=8)
            ctk.CTkLabel(info, text=path.name, text_color=self.TEXT,
                         font=ctk.CTkFont("Segoe UI", 11, weight="bold"),
                         anchor="w").pack(fill="x")
            size_kb = path.stat().st_size / 1024 if path.exists() else 0
            ctk.CTkLabel(info, text=f"{size_kb:.1f} KB  •  {path.parent}", text_color=self.MUTED,
                         font=ctk.CTkFont("Segoe UI", 8), anchor="w",
                         wraplength=205).pack(fill="x", pady=(2, 0))
            ctk.CTkButton(row, text="×", width=28, height=28, corner_radius=7,
                          fg_color="transparent", hover_color="#633747",
                          text_color="#F28A9B", font=ctk.CTkFont(size=17),
                          command=lambda i=index: self._remove_file(i)).pack(side="right", padx=7)
        if not self.selected_files:
            ctk.CTkLabel(self.file_list, text="No files imported yet.\nClick Import CSV files.",
                         text_color=self.MUTED, justify="center",
                         font=ctk.CTkFont("Segoe UI", 11)).pack(expand=True, pady=30)

    def _select_files(self) -> None:
        paths = filedialog.askopenfilenames(title="Select CSV files",
                                             filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        added = 0
        for item in paths:
            path = Path(item)
            if path not in self.selected_files:
                self.selected_files.append(path)
                added += 1
        self._refresh_files()
        self._set_status(f"Added {added} file(s). {len(self.selected_files)} selected.")

    def _remove_file(self, index: int) -> None:
        if 0 <= index < len(self.selected_files):
            removed = self.selected_files.pop(index)
            self._refresh_files()
            self._set_status(f"Removed {removed.name} from the import list.")

    def _clear_files(self) -> None:
        self.selected_files.clear()
        self._refresh_files()
        self._set_status("Import list cleared.")

    def _merge(self) -> None:
        if not self.selected_files:
            messagebox.showwarning("No files", "Import at least one CSV file first.")
            return
        try:
            headers, rows = [], []
            for path in self.selected_files:
                file_headers, file_rows, _ = read_csv(path)
                for header in file_headers:
                    if header not in headers:
                        headers.append(header)
                rows.extend(file_rows)
            self.output_headers, self.output_rows = headers, rows
            self.last_removed = 0
            self._refresh_preview()
            self._set_status(f"Successfully merged {len(self.selected_files)} file(s).")
        except (ValueError, OSError) as exc:
            messagebox.showerror("Could not merge CSV files", str(exc))
            self._set_status("Merge failed. Check the selected files.")

    def _dedupe(self) -> None:
        if not self.output_headers:
            messagebox.showwarning("No result", "Merge files before removing duplicates.")
            return
        self.output_rows, removed = remove_duplicates(self.output_rows, self.output_headers)
        self.last_removed += removed
        self._refresh_preview()
        self._set_status(f"Removed {removed} duplicate row(s).")

    def _refresh_preview(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = self.output_headers
        for header in self.output_headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, width=max(120, min(230, len(header) * 12 + 35)), anchor="w")
        for row in self.output_rows[:500]:
            self.tree.insert("", "end", values=[row.get(h, "") for h in self.output_headers])
        self.stat_values["rows"].configure(text=str(len(self.output_rows)))
        self.stat_values["columns"].configure(text=str(len(self.output_headers)))
        self.stat_values["duplicates"].configure(text=str(self.last_removed))
        shown = min(500, len(self.output_rows))
        self.preview_hint.configure(text=f"Showing {shown} of {len(self.output_rows)} rows")

    def _export(self) -> None:
        if not self.output_headers:
            messagebox.showwarning("No result", "Merge CSV files before exporting.")
            return
        destination = filedialog.asksaveasfilename(
            title="Export merged CSV", defaultextension=".csv",
            initialfile="smartfile_result.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not destination:
            return
        try:
            write_csv(Path(destination), self.output_headers, self.output_rows, delimiter=';')
            self._set_status(f"Exported {len(self.output_rows)} row(s) to {destination}")
            messagebox.showinfo("Export complete", f"Your CSV was saved successfully:\n{destination}")
        except (ValueError, OSError) as exc:
            messagebox.showerror("Export failed", str(exc))
            self._set_status("Export failed.")


def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = DnDCTk()
    SmartFileApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
