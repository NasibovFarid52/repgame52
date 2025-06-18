def apply_gravity(entity, platforms):

    entity.velocity.y += GRAVITY
    entity.rect.y += entity.velocity.y

    # Проверка коллизий с платформами
    collisions = pygame.sprite.spritecollide(entity, platforms, False)
    for platform in collisions:
        if entity.velocity.y > 0:  # Падение вниз
            entity.rect.bottom = platform.rect.top
            entity.velocity.y = 0
            if hasattr(entity, 'on_ground'):
                entity.on_ground = True
        elif entity.velocity.y < 0:  # Движение вверх
            entity.rect.top = platform.rect.bottom
            entity.velocity.y = 0


def check_horizontal_collision(entity, platforms):

    entity.rect.x += entity.velocity.x
    collisions = pygame.sprite.spritecollide(entity, platforms, False)
    for platform in collisions:
        if entity.velocity.x > 0:  # Движение вправо
            entity.rect.right = platform.rect.left
        elif entity.velocity.x < 0:  # Движение влево
            entity.rect.left = platform.rect.right
    return collisions