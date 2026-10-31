import cv2

def draw(frame, objects, speeds, total_count, friction_events):
    h, w = frame.shape[:2]

    # Dynamically scale font, line thickness, and padding based on frame resolution
    font_scale = max(0.5, (w / 1280.0) * 0.55)
    thickness = max(1, int((w / 1280.0) * 2))
    hud_font_scale = max(0.6, (w / 1280.0) * 0.7)

    # --- 1. Draw Tracked Vehicle Bounding Boxes & Labels ---
    for obj_id, (cx, cy, det) in objects.items():
        x1, y1, x2, y2, label, conf = det

        box_color = (0, 255, 0)  # Green
        warning_text = ""

        if obj_id in friction_events:
            box_color = (0, 0, 255)  # Red
            warning_text = f" [{friction_events[obj_id]}]"

        accuracy_pct = int(conf * 100)
        text = f"{label} ({accuracy_pct}%) {speeds.get(obj_id, 0)} km/h{warning_text}"

        # Draw vehicle bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, thickness)

        # Calculate exact label dimensions for high-contrast background box
        (text_w, text_h), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
        )
        
        # Keep text label inside the top frame border if vehicle is at the top edge
        label_y1 = max(y1 - text_h - 10, 0)
        
        # Draw solid background box behind label text
        cv2.rectangle(
            frame, 
            (x1, label_y1), 
            (x1 + text_w + 10, label_y1 + text_h + baseline + 6), 
            box_color, 
            -1
        )
        
        # Render high-contrast text on top of the solid label background box
        text_color = (255, 255, 255) if box_color == (0, 0, 255) else (0, 0, 0)
        cv2.putText(
            frame, 
            text, 
            (x1 + 5, label_y1 + text_h + 2), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            font_scale, 
            text_color, 
            thickness, 
            cv2.LINE_AA
        )

    # --- 2. Live Count & Congestion HUD Panel ---
    if total_count >= 8:
        status = "HEAVY TRAFFIC"
        status_color = (0, 0, 255)    # Red
    elif total_count >= 4:
        status = "MODERATE TRAFFIC"
        status_color = (0, 255, 255)  # Yellow
    else:
        status = "SMOOTH FLOW"
        status_color = (0, 255, 0)    # Green

    has_friction = len(friction_events) > 0
    lines = [
        (f"Live Count: {total_count}", (255, 255, 255)),
        (f"Status: {status}", status_color)
    ]

    if total_count >= 6 and has_friction:
        lines.append(("HIGH RISK BOTTLENECK!", (0, 0, 255)))

    # Calculate dynamic HUD panel size based on longest text line
    max_text_w = 0
    line_metrics = []

    for line_text, _ in lines:
        (tw, th), base = cv2.getTextSize(
            line_text, cv2.FONT_HERSHEY_SIMPLEX, hud_font_scale, thickness
        )
        max_text_w = max(max_text_w, tw)
        line_metrics.append((th, base))

    padding = int(15 * (w / 1280.0))
    padding = max(10, padding)

    hud_w = max_text_w + (padding * 2)
    
    # Calculate height of all lines combined
    total_text_h = sum(h + b + int(8 * (w / 1280.0)) for h, b in line_metrics)
    hud_h = total_text_h + padding

    # Draw dark overlay HUD panel
    cv2.rectangle(frame, (padding, padding), (padding + hud_w, padding + hud_h), (0, 0, 0), -1)
    cv2.rectangle(frame, (padding, padding), (padding + hud_w, padding + hud_h), (80, 80, 80), thickness)

    # Render HUD text line by line
    current_y = padding
    for idx, (line_text, line_color) in enumerate(lines):
        th, base = line_metrics[idx]
        current_y += th + int(6 * (w / 1280.0))
        cv2.putText(
            frame, 
            line_text, 
            (padding + int(10 * (w / 1280.0)), current_y), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            hud_font_scale, 
            line_color, 
            thickness, 
            cv2.LINE_AA
        )
        current_y += base + int(4 * (w / 1280.0))

    return frame