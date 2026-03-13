// KubeJS server-side script
// Lightweight recurring event messaging for Cobblemon progression loops.

ServerEvents.loaded((event) => {
  console.log('[CobblemonEvents] Loaded recurring event announcer script.')
})

const EVENT_ROTATION = [
  'Outbreak Hour starts in 10 minutes at /warp outbreak!',
  'Gym Challenge Window is open now. Talk to the Gym NPC at spawn.',
  'Catch Contest is active for 30 minutes. Check /spawn board for species.',
]

let rotationIndex = 0

ServerEvents.tick((event) => {
  const server = event.server

  // Every 15 minutes (20 ticks * 60 sec * 15)
  if (server.overworld().gameTime % 18000 !== 0) {
    return
  }

  const message = EVENT_ROTATION[rotationIndex]
  rotationIndex = (rotationIndex + 1) % EVENT_ROTATION.length

  server.tell(Text.gold('[Events] ').append(Text.white(message)))
})
