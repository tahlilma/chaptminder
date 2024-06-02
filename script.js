const repeater = new Timer();
repeater.repeats = true;
repeater.timeInterval = 3600000;

repeater.schedule(async () => {

  let req = new Request(
    "https://chaptminder-tahlil-0a4a4164.koyeb.app/get_updates"
  );

  let data = await req.loadJSON();
  console.log(data);

  const widget = new ListWidget();

  widget.addDate(new Date());

  let gradient = new LinearGradient();
  gradient.locations = [0, 1];
  gradient.colors = [new Color("4286F4"), new Color("373B44")];

  widget.backgroundGradient = gradient;

  let title = widget.addText("New Chapters:");
  title.font = Font.lightRoundedSystemFont(30);

  let count = widget.addText(`${data.count}`);
  count.font = Font.heavyMonospacedSystemFont(60);

  Script.setWidget(widget);

});
