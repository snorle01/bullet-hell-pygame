def collide(obj1, obj2):
    if obj1.rect.colliderect(obj2.rect):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None