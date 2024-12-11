#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::{Manager, Runtime};
use window_vibrancy::{apply_vibrancy, NSVisualEffectMaterial};
use cocoa::appkit::{NSWindowTitleVisibility, NSWindowStyleMask};
use cocoa::base::{id, nil, YES};
use objc::{msg_send, sel, sel_impl};
use dotenv::dotenv;
use std::env;

// This command is specific to macOS
#[tauri::command]
fn toggle_fullscreen<R: Runtime>(window: tauri::Window<R>) {
    if let Ok(ns_window) = window.ns_window() {
        unsafe {
            let _: () = msg_send![ns_window as id, toggleFullScreen: nil];
        }
    }
}

// This command handles the window titlebar on macOS
#[tauri::command]
fn toggle_titlebar<R: Runtime>(window: tauri::Window<R>, show: bool) {
    if let Ok(ns_window) = window.ns_window() {
        unsafe {
            if show {
                let _: () = msg_send![ns_window as id, setTitlebarAppearsTransparent: YES];
                let _: () = msg_send![ns_window as id, setTitleVisibility: NSWindowTitleVisibility::NSWindowTitleVisible];
            } else {
                let _: () = msg_send![ns_window as id, setTitlebarAppearsTransparent: YES];
                let _: () = msg_send![ns_window as id, setTitleVisibility: NSWindowTitleVisibility::NSWindowTitleHidden];
            }
        }
    }
}

#[tauri::command]
fn get_api_key() -> String {
    env::var("ANTHROPIC_API_KEY")
        .expect("ANTHROPIC_API_KEY must be set in .env file")
}

fn main() {
    // Load .env file
    dotenv().ok();

    // Retrieve the API key
    let api_key = env::var("ANTHROPIC_API_KEY")
        .expect("ANTHROPIC_API_KEY must be set");

    let context = tauri::generate_context!();
    tauri::Builder::default()
        .setup(|app| {
            let window = app.get_window("main").unwrap();
            
            #[cfg(target_os = "macos")]
            {
                // Add vibrancy effect for macOS
                apply_vibrancy(&window, NSVisualEffectMaterial::HudWindow, None, None)
                    .expect("Failed to add vibrancy effect");

                // Configure window for macOS
                if let Ok(ns_window) = window.ns_window() {
                    unsafe {
                        let _: () = msg_send![ns_window as id, setTitlebarAppearsTransparent: YES];
                        let style_mask: NSWindowStyleMask = msg_send![ns_window as id, styleMask];
                        let new_style_mask = style_mask | NSWindowStyleMask::NSFullSizeContentViewWindowMask;
                        let _: () = msg_send![ns_window as id, setStyleMask: new_style_mask];
                        let _: () = msg_send![ns_window as id, setRestorable: YES];
                    }
                }
            }

            // Enable devtools in debug mode
            #[cfg(debug_assertions)]
            window.open_devtools();

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![toggle_fullscreen, toggle_titlebar, get_api_key])
        .run(context)
        .expect("error while running tauri application");
}