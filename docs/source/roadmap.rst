Roadmap
=======

Possible future development of the package may include:

1. The package currently only considers ``Enum`` classes. No consideration has been given to the other enum classes (ie: ``IntEnum``, ``IntFlag``, ``Flag``). Behaviour with these enum types is undefined.
2. When using :func:`~extendableenum.copy_enum_members`, copied members could be handled more intelligently. Currently it is the user's responsibility to manage name/value conflicts. If the values don't matter (eg: use of `auto <https://docs.python.org/3/library/enum.html#enum.auto>`_) this may be handled more intelligenty/automatically.