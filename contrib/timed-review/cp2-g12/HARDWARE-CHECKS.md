# Hardware checks before an upstream PR or product qualification

Use one explicitly authorized, identified unit first. Preserve its data and a
recovery path. Record model/revision/panel, firmware hash, source refs and method.
Do not substitute X4 Pro for original X4/C3.

1. Off: ordinary reading, sleep and Power wake retain the same book position.
2. Local: both wallpaper roots; repeated wake/paint/sleep, no reader-state write;
   invalid/truncated images and missing directories; return to ordinary reading.
3. Plugin: exactly one handler, valid CA/grant/config and saved network; A to B,
   bad peer/CA, invalid BMP, 503/offline and last-good, rearm and Off.
4. Power: press during the connection/body/panel interval, then confirm the same
   book page. USB navigation does not exercise the physical Power path.
5. Battery: unplug only the selected reader and observe autonomous cycles.
   Measure elapsed wake-to-sleep and current separately from the retained image.
6. C3 memory: free internal heap and largest contiguous block before radio,
   during the handshake, during decode and after repeated teardown. Include the
   normal font/display context. Host memory is not a substitute.
7. PaperMono: RTC/PMIC wake and button priority; keep brownout detection on.
   Fault injection must distinguish inaccessible RTC from unknown PMIC wake-route
   state. The host regression is not proof of a physical I2C fault scenario.
8. Update/recovery: preserve books, settings, active plugin root, token/config and
   normal firmware update channel; restore the agreed data and release USB.

Record PASS/FAIL/NOT MEASURED per case. Scope orientation, grayscale and touch
claims to the actually exercised profile; one successful model does not qualify
all three. A persistent last-good image does not itself show that the device is awake.
