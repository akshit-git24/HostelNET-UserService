from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from .kafka_producer import KafkaProducer

@receiver(post_save, sender=User)
def publish_user_save(sender, instance, created, **kwargs):
    producer = KafkaProducer()
    event_type = 'UserCreated' if created else 'UserUpdated'
    
    data = {
        'event': event_type,
        'user_id': instance.id,
        'username': instance.username,
        'email': instance.email,
        'role': instance.role
    }
    
    print(f"DEBUG: Signal triggered for {instance.username}, sending data...", flush=True)
    producer.produce_message('user-events', data)


@receiver(post_delete, sender=User)
def publish_user_delete(sender, instance, **kwargs):
    producer = KafkaProducer()
    data = {
        'event': 'UserDeleted',
        'user_id': instance.id,
        'username': instance.username # Just for reference
    }
    producer.produce_message('user-events', data)
