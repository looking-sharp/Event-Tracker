function seedTestData(userId, numEvents = 3, numRsvps = 5) {
  fetch("/api/seed_test_data", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      user_id: userId,
      events: numEvents,
      rsvps: numRsvps
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      console.error("Error:", data.error);
    } else {
      console.log("Success:", data.message);
      console.log("Event IDs:", data.events);
    }
  })
  .catch(err => {
    console.error("Request failed:", err);
  });
}
